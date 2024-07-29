import ckan.plugins.toolkit as tk
import ckan.authz as authz
import ckan.logic.auth as logic_auth
from ckanext.theme_sddi.logic import restricted_check_user_resource_access, restricted_get_username_from_context


@tk.chained_auth_function
@tk.auth_allow_anonymous_access
def resource_show(next_auth, context, data_dict=None):

    # Ensure user who can edit the package can see the resource
    # breakpoint()
    resource = data_dict.get('resource', context.get('resource', {}))
    if not resource:
        resource = logic_auth.get_resource_object(context, data_dict)
    if type(resource) is not dict:
        resource = resource.as_dict()

    if authz.is_authorized(
            'package_update', context,
            {'id': resource.get('package_id')}).get('success'):
        return ({'success': True})

    user_name = restricted_get_username_from_context(context)

    package = data_dict.get('package', {})
    if not package:
        model = context['model']
        package = model.Package.get(resource.get('package_id'))
        package = package.as_dict()

    authodized = restricted_check_user_resource_access(
        user_name, resource, package)
    if not authodized:
        return {'success': False, 'msg': 'Not authorized'}
    return next_auth(context, data_dict)
