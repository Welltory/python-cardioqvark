#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_python_cardioqvark
----------------------------------

Tests for `python_cardioqvark` module.
"""

from python_cardioqvark import CardioQVARKClient


class TestPythonCardioQVARKApiClient(object):
    @classmethod
    def setup_class(cls):
        cls.test_client = CardioQVARKClient(
            client_id=4450,
            client_password='testpassword')
        print(cls.test_client)

    def test_client_settings(self):
        assert self.test_client.api_server_url
        assert self.test_client.cloud_server_url

    def test_client_get_all_cardiograms(self):
        cardiograms = self.test_client.get_cardiogram()
        assert cardiograms

    def test_client_get_patient(self):
        patient = self.test_client.get_patient(1004)
        assert patient != {}

    def test_client_get_analysis(self):
        patient = self.test_client.get_analysis(1004)
        assert patient != {}
