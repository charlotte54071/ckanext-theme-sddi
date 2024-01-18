from flask import Blueprint


theme_sddi = Blueprint(
    "theme_sddi", __name__)


def page():
    return "Hello, theme_sddi!"


theme_sddi.add_url_rule(
    "/theme_sddi/page", view_func=page)


def get_blueprints():
    return [theme_sddi]
