import ckan.plugins.toolkit as tk
import ckanext.theme_sddi.logic.schema as schema


@tk.side_effect_free
def theme_sddi_get_sum(context, data_dict):
    tk.check_access(
        "theme_sddi_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.theme_sddi_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'theme_sddi_get_sum': theme_sddi_get_sum,
    }
