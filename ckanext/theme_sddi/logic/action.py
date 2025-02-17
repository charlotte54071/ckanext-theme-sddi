import logging
import json

import ckan.model as model
import ckan.authz as authz
import ckan.plugins.toolkit as tk
import ckan.logic.schema as schema_
import ckan.logic as ckan_logic

from ckan.lib.mailer import mail_recipient
from ckan.lib.mailer import MailerException

import ckanext.theme_sddi.logic.auth as auth
import ckanext.theme_sddi.logic as logic
from ckanext.theme_sddi.logic import (
    restricted_get_username_from_context,
    restricted_get_restricted_dict,
    restricted_check_user_resource_access,
)

log = logging.getLogger(__name__)


_get_or_bust = tk.get_or_bust


@tk.side_effect_free
def group_tree_children_g(context, data_dict):
    """Returns a flat list of groups of the children of the group
    identified by parameter id in data_dict.

    :param id: the id or name of the parent group.
    :param type: "group"
    :returns: list of children GroupTreeNodes

    """
    root_group = _group_tree_check_g(data_dict)
    children = root_group.get_children_group_hierarchy(type=root_group.type)
    children = [
        {"id": id, "name": name, "title": title} for id, name, title, _ in children
    ]
    return children


def _group_tree_check_g(data_dict):
    group_name_or_id = _get_or_bust(data_dict, "id")
    group = model.Group.get(group_name_or_id)
    if group is None:
        raise tk.ObjectNotFound
    group_type = data_dict.get("type", "groups")
    if group.type != group_type:
        how_type_was_set = (
            "was specified" if data_dict.get("type") else "is filtered by default"
        )
        raise tk.ValidationError(
            'Group type is "{}" not "{}" that {}'.format(
                group.type, group_type, how_type_was_set
            )
        )
    return group


@tk.chained_action
def user_create(original_action, context, data_dict):
    group_list = tk.get_action("group_list")({}, {})
    site_user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    user = original_action(context, data_dict)

    role = tk.config.get("ckan.userautoadd.organization_role", "member")
    context["user"] = site_user.get("name")

    for group in group_list:
        try:
            tk.get_action("group_show")(
                context,
                {
                    "id": group,
                },
            )
        except logic.NotFound:
            return user

        tk.get_action("group_member_create")(
            context,
            {
                "id": group,
                "username": user["name"],
                "role": role,
            },
        )

    return user


@tk.chained_action
def user_update(next, context, data_dict):
    last_attempt_time = data_dict.get("last_attempt_time")
    if last_attempt_time:
        not_empty = tk.get_validator("not_empty")
        unicode_safe = tk.get_validator("unicode_safe")
        schema = context.get("schema") or schema_.default_update_user_schema()
        schema["last_attempt_time"] = [not_empty, unicode_safe]

        plugin_extras = {
            "sddi": {
                "last_attempt_time": json.dumps(
                    last_attempt_time, indent=4, sort_keys=True, default=str
                )
            }
        }

        data_dict = dict(data_dict, plugin_extras=plugin_extras)
        return next(context, data_dict)

    return next(context, data_dict)


# Restricted actions
def restricted_user_create_and_notify(context, data_dict):

    def body_from_user_dict(user_dict):
        body = ""
        for key, value in user_dict.items():
            body += "* {0}: {1}\n".format(
                key.upper(), value if isinstance(value, str) else str(value)
            )
        return body

    user_dict = user_create(context, data_dict)

    # Send your email, check ckan.lib.mailer for params
    try:
        name = tk._("CKAN System Administrator")
        email = tk.config.get("email_to")
        if not email:
            raise MailerException('Missing "email-to" in config')

        subject = tk._("New Registration: {0} ({1})").format(
            user_dict.get("name", tk._("new user")), user_dict.get("email")
        )

        extra_vars = {
            "site_title": tk.config.get("ckan.site_title"),
            "site_url": tk.config.get("ckan.site_url"),
            "user_info": body_from_user_dict(user_dict),
        }

        body = tk.render("restricted/emails/restricted_user_registered.txt", extra_vars)

        mail_recipient(name, email, subject, body)

    except MailerException as mailer_exception:
        log.error("Cannot send mail after registration")
        log.error(mailer_exception)

    return user_dict


@tk.side_effect_free
@tk.chained_action
def resource_view_list(original_action, context, data_dict):
    model = context["model"]
    id = _get_or_bust(data_dict, "id")
    resource = model.Resource.get(id).as_dict()
    if not resource:
        raise tk.ObjectNotFound
    try:
        tk.check_access(
            "resource_view_list",
            context,
            {"id": resource.get("id"), "resource": resource},
        )
    except tk.NotAuthorized:
        return []
    else:
        return original_action(context, data_dict)


@tk.chained_action
def resource_search(original_action, context, data_dict):
    resource_search_result = original_action(context, data_dict)

    restricted_resource_search_result = {}

    for key, value in resource_search_result.items():
        if key == "results":
            # restricted_resource_search_result[key] = \
            #     _restricted_resource_list_url(context, value)
            restricted_resource_search_result[key] = _resource_list_hide_fields(
                context, value
            )
        else:
            restricted_resource_search_result[key] = value

    return restricted_resource_search_result


@tk.side_effect_free
def restricted_check_access(context, data_dict):
    if not data_dict:
        return
    package_id = data_dict.get("id", False)
    resource_id = data_dict.get("resource").get("id") or False

    user_name = logic.restricted_get_username_from_context(context)

    if not package_id:
        raise tk.ValidationError("Missing package_id")
    if not resource_id:
        raise tk.ValidationError("Missing resource_id")

    log.debug("action.restricted_check_access: user_name = " + str(user_name))

    log.debug("checking package " + str(package_id))
    package_dict = tk.get_action("package_show")(
        dict(context, return_type="dict"), {"id": package_id}
    )
    log.debug("checking resource")
    resource_dict = tk.get_action("resource_show")(
        dict(context, return_type="dict"), {"id": resource_id}
    )

    return logic.restricted_check_user_resource_access(
        user_name, resource_dict, package_dict
    )


def _resource_list_hide_fields(resource_list):
    restricted_resources_list = []

    for resource in resource_list:
        # Copy original resource to avoid modifying the input
        restricted_res = dict(resource)

        try:
            # Get the restricted fields
            restricted_dict = logic.restricted_get_restricted_dict(restricted_res)

            # Skip processing if no restricted dict is found
            if not restricted_dict:
                restricted_resources_list.append(restricted_res)
                continue

            context = {"user": tk.g.user, "model": model}
            package_id = resource.get("package_id")

            # Skip processing if no package_id is found
            if not package_id:
                restricted_resources_list.append(restricted_res)
                continue

            try:
                is_authorized = authz.is_authorized(
                    "package_update", context, {"id": package_id}
                ).get("success", False)
            except logic.NotFound:
                # If package not found, treat as unauthorized
                is_authorized = False

            # Only modify restricted fields for unauthorized users
            if not is_authorized:
                user_name = logic.restricted_get_username_from_context()

                # Process allowed users list
                allowed_users = []
                for user in restricted_dict.get("allowed_users", []):
                    user = user.strip()
                    if user:
                        if user_name == user:
                            allowed_users.append(user_name)
                        else:
                            # Mask other usernames
                            allowed_users.append(f"{user[:3]}*****{user[-2:]}")

                # Create new restricted dict
                new_restricted = json.dumps(
                    {
                        "level": restricted_dict.get("restricted_level"),
                        "allowed_users": ",".join(allowed_users),
                    }
                )

                # Update restricted field in extras if it exists
                extras = restricted_res.get("extras", {})
                if extras and "restricted" in extras:
                    restricted_res["extras"]["restricted"] = new_restricted

                # Update top-level restricted field if it exists
                if "restricted" in restricted_res:
                    restricted_res["restricted"] = new_restricted

        except Exception as e:
            # Log any errors but continue processing other resources
            log.error(f"Error processing resource restrictions: {str(e)}")
            # Add the original resource without modifications
            restricted_res = dict(resource)

        restricted_resources_list.append(restricted_res)

    return restricted_resources_list
