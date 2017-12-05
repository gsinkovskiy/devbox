import click


@click.group(name='routes')
def commands():
    pass


@commands.command(name='routes:update')
@click.argument('container', nargs=-1)
def execute(container=None):
    """
    Update network routes
    """
    # print(container)

    # TODO: implement
    click.echo('Update routes')
    # route /P add 172.26.0.0 MASK 255.255.0.0 10.0.75.2
