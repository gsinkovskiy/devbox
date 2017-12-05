import click


@click.group(name='devbox')
def commands():
    pass


@commands.command(name='devbox:update')
def execute():
    """
    Update devbox
    """
    click.echo('update!')
    # TODO: implement
