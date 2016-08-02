# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import BaseAPIClient


class CardioQVARKClient(BaseAPIClient):
    def get_cardiogram(self, _id):
        url = '/cardiogram/{}'.format(_id)
        result = self._call_api_method(url=url, server=self.api_server_url)
        return result.json()

    def get_patient(self, _id):
        url = '/profile/{}'.format(_id)
        result = self._call_api_method(url=url)
        return result.json()

    def get_analysis(self, _id):
        url = '/analysis/{}/vsr'.format(_id)
        result = self._call_api_method(url=url)
        return result.json()
