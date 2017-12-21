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
    from ...utils.docker import DockerHelper, get_compose_project_name
    from docker.errors import NotFound

    docker_helper = DockerHelper()

    volume_name = volume
    try:
        docker_helper.get_volume(volume_name)
    except NotFound:
        compose_project = get_compose_project_name()
        volume_name = docker_helper.get_full_volume_name(volume, compose_project)

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
    # TODO: restart projects
    from ..up import execute as up
    ctx.invoke(up)
