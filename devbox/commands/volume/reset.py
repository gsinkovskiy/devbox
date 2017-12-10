import click


@click.group(name='volume')
def commands():
    pass


@commands.command(name='volume:reset')
@click.argument('volume')
@click.pass_context
def execute(ctx, volume):
    """
    Resets given volume (remove and recreate)
    """
    click.echo('Reset volume')

    from devbox.utils.docker import DockerHelper

    docker_helper = DockerHelper()

    volume_name = docker_helper.get_full_volume_name(volume)
    if not volume_name:
        click.echo('Could not find volume "{0}".'.format(volume))

        return None

    used_containers = docker_helper.get_used_containers_for_volume(volume_name)

    for used_container in used_containers:
        click.echo('Stop container "{0}"'.format(used_container.name))
        used_container.stop()
        click.echo('Remove container "{0}"'.format(used_container.name))
        used_container.remove()

    click.echo('Remove volume "{0}"'.format(volume_name))
    docker_helper.get_volume(volume_name).remove(force=True)

    click.echo('Restart devbox')
    from devbox.commands.up import execute as up
    ctx.invoke(up)
