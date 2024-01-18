"""Tests for helpers.py."""

import ckanext.theme_sddi.helpers as helpers


def test_theme_sddi_hello():
    assert helpers.theme_sddi_hello() == "Hello, theme_sddi!"
