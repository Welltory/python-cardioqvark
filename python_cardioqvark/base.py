# -*- coding: utf-8 -*-
import shutil
import tempfile
from urlparse import urljoin

import requests

from python_cardioqvark.consts import API_BASE_URL
from python_cardioqvark.exceptions import CACertificateException


class BaseAPIClient(object):
    def __init__(self, client_id, client_password, path_to_client_cert):
        self.client_id = client_id
        self.client_password = client_password
        self.path_to_client_cert = path_to_client_cert
        self.__download_ca()

    @staticmethod
    def __get_full_url(url):
        return urljoin(API_BASE_URL, url)

    def __download_ca(self):
        url = self.__get_full_url('/ca?media=PEM')
        r = requests.get(url)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        else:
            raise CACertificateException('Could not download CA certificate')

    def _get(self, url):
        full_url = urljoin(API_BASE_URL, url)
        response = requests.get(
            full_url,
            verify=False,
            cert=self.path_to_client_cert
        )

        return response.json()
