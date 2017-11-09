import click

@click.group(name='routes')
def commands():
    pass

@commands.command(name='routes:update')
@click.argument('container', nargs=-1)
def execute(container = None):
    """
    Update network routes
    """
    #print(container)
    from devbox.utils import admin, docker as docker_utils
    import docker

    # TODO: implement
    click.echo('Update routes')
    # route /P add 172.18.0.0 MASK 255.255.0.0 10.0.75.2
