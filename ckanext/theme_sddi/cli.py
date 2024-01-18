import click


@click.group(short_help="theme_sddi CLI.")
def theme_sddi():
    """theme_sddi CLI.
    """
    pass


@theme_sddi.command()
@click.argument("name", default="theme_sddi")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [theme_sddi]
