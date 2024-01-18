"""Tests for views.py."""

import pytest

import ckanext.theme_sddi.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "theme_sddi")
@pytest.mark.usefixtures("with_plugins")
def test_theme_sddi_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("theme_sddi.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, theme_sddi!"
