"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.theme_sddi.logic import validators


def test_theme_sddi_reauired_with_valid_value():
    assert validators.theme_sddi_required("value") == "value"


def test_theme_sddi_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.theme_sddi_required(None)
