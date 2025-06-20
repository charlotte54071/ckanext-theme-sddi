from ckan.plugins import toolkit

def update_config(config):
    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('public', 'theme-sddi')   
