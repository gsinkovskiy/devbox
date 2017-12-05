import click


@click.group(name='volume')
def commands():
    pass


@commands.command(name='volume:reset')
@click.argument('volume')
@click.pass_context
def execute(ctx, volume):
    """
    Resets given volume
    """
    click.echo('Reset volume')

    # sphinxsearch - data - volume

    import docker

    volume_name = None
    client = docker.from_env()
    for docker_volume in client.volumes.list():
        if not docker_volume.attrs['Labels']:
            continue

        if docker_volume.attrs['Labels']['com.docker.compose.volume'] == volume:
            volume_name = docker_volume.attrs['Name']

    if not volume_name:
        click.echo('Could not find volume "{0}".'.format(volume))

        return None

    used_containers = list()
    for container in client.containers.list(all=True):
        for mount in container.attrs['Mounts']:
            if not 'Name' in mount:
                continue

            if mount['Name'] == volume_name:
                used_containers.append(container)

    for used_container in used_containers:
        click.echo('Stop container')
        used_container.stop()
        used_container.remove()

    click.echo('Remove volume')
    client.volumes.get(volume_name).remove(force=True)

    click.echo('Restart devbox')
    from devbox.commands.up import execute as up
    ctx.invoke(up)
