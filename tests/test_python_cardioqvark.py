#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_python_cardioqvark
----------------------------------

Tests for `python_cardioqvark` module.
"""

from python_cardioqvark import BaseAPIClient


class TestPython_cardioqvark(object):
    @classmethod
    def setup_class(cls):
        cls.test_client = BaseAPIClient(client_id=4450,
                                        client_password='testpassword',
                                        path_to_client_cert='/tmp/test')

    def test_something(self):
        print(self.test_client)

    @classmethod
    def teardown_class(cls):
        pass
