# -*- coding: utf-8 -*-
import os
import re
import tempfile
from itertools import cycle
from urlparse import urljoin

import requests
import ujson as json

from .consts import API_BASE_URL, QVARK_CA_CERT_NAME, CLIENT_CERT_PATH
from .exceptions import CACertificateException, CardioQVARKException

QVARK_CA_CERT_PATH = os.path.join('/tmp/', QVARK_CA_CERT_NAME)


class BaseAPIClient(object):
    client_id = None
    client_password = None
    role_id = None

    path_to_client_cert = None
    path_to_qvark_cert = None

    settings = None

    cloud_server_url = None

    __api_server_urls = []
    __cloud_server_urls = []

    def __init__(self, client_id, client_password, role_id=3,
                 path_to_client_cert=None):
        self.client_id = client_id
        self.client_password = client_password
        self.role_id = role_id

        if path_to_client_cert:
            self.path_to_client_cert = path_to_client_cert
        else:
            self.__download_client_cert()

        self.__download_ca()
        self.__create_full_client_cert()
        self.__set_settings()

    def __repr__(self):
        return 'Client for CardioQVARK API with client_id: {}'.format(
            self.client_id
        )

    @property
    def api_server_url(self):
        if self.__api_server_urls:
            return next(self.__api_server_urls)
        return None

    @property
    def cloud_server_url(self):
        if self.__cloud_server_urls:
            return next(self.__cloud_server_urls)
        return None

    @staticmethod
    def __get_full_url(server, url, port=1443):
        if not server.startswith('https'):
            server = 'https://{}:{}/'.format(server, port)
        return urljoin(server, url)

    def __download_ca(self):
        url = self.__get_full_url(API_BASE_URL, '/ca?media=PEM')
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            with open(QVARK_CA_CERT_PATH, 'wb') as f:
                f.write(r.content)
                self.path_to_qvark_cert = f.name
        else:
            raise CACertificateException('Could not download CA certificate')

    def __download_client_cert(self):
        url = self.__get_full_url(API_BASE_URL, '/account?media=PEM')
        client_cert_full_path = os.path.join(CLIENT_CERT_PATH,
                                             '{}.pem'.format(self.client_id))
        payload = {
            'id': self.client_id,
            'password': self.client_password,
            'role': self.role_id
        }
        r = requests.post(url, verify=False, data=json.dumps(payload))

        if r.status_code == 200:
            with open(client_cert_full_path, 'wb') as client_cert:
                client_cert.write(r.content)
                self.path_to_client_cert = client_cert.name
        else:
            raise CardioQVARKException('Could not download client '
                                       'certificate: {}'.format(r.status_code))

    def __create_full_client_cert(self):
        with tempfile.NamedTemporaryFile(delete=False) as full_client_cert:
            with open(self.path_to_client_cert, 'r') as client_cert:
                full_client_cert.write(client_cert.read())

            with open(self.path_to_qvark_cert, 'r') as qvark_cert:
                full_client_cert.write(qvark_cert.read())

            self.path_to_full_client_cert = full_client_cert.name

    def __set_settings(self):
        r = self._call_api_method('/settings')
        if r.status_code != 200:
            raise CardioQVARKException(r.status_code)

        result = r.json()
        self.__api_server_urls = cycle(result['api'])
        self.__cloud_server_urls = cycle(result['cloud'])

    def _call_api_method(self, url, method='GET', server=None, headers=None,
                         **params):
        if headers is None:
            headers = {}
        server = server or self.api_server_url or API_BASE_URL

        full_url = self.__get_full_url(server, url)
        response = requests.request(
            method=method,
            url=full_url,
            verify=False,
            cert=self.path_to_full_client_cert,
            timeout=1,
            params=params,
            headers=headers
        )

        print(response.headers)

        if response.status_code != 200:
            raise CardioQVARKException(response.raw)

        return response

    def _parse_response_headers(self, headers):
        result = {}
        if 'content-range' in headers.keys():
            _from, _to, _max = re.findall('\d+', headers['content-range'])
            result.update({
                'range_start': _from,
                'range_end': _to,
                'max': _max
            })

        return result
