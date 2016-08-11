# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseAPIClient


class CardioQVARKClient(BaseAPIClient):
    def get_cardiogram(self, _id='', range_start=None, range_end=None,
                       **params):
        url = '/cardiogram/{}'.format(_id)
        headers = {}
        if range_start and range_end:
            headers['Range'] = 'items={}-{}'.format(
                range_start,
                range_end
            )
        response = self._call_api_method(
            url=url,
            server=self.api_server_url,
            headers=headers,
            **params
        )

        result = self._parse_response_headers(response.headers)
        result.update({
            'data': response.json()
        })
        return result

    def get_patient(self, _id='', range_start=None, range_end=None, **params):
        url = '/profile/{}'.format(_id or '')
        headers = {}
        if range_start and range_end:
            headers['Range'] = 'items={}-{}'.format(
                range_start,
                range_end
            )
        response = self._call_api_method(url=url, **params)
        result = self._parse_response_headers(response.headers)
        result.update({
            'data': response.json()
        })
        return result

    def get_analysis(self, _id, **params):
        url = '/analysis/{}/vsr'.format(_id)
        result = self._call_api_method(url=url, **params)
        return result.json()
