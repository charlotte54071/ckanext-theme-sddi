import ckan.plugins.toolkit as tk


def theme_sddi_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "theme_sddi_required": theme_sddi_required,
    }
