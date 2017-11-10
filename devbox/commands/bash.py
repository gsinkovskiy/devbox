import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='bash')
@click.argument('service', required=False)
@click.pass_context
def execute(ctx, service):
    """
    Open bash on the given service
    """
    from subprocess import call
    from devbox.utils.docker import get_default_service

    from devbox.utils.cwd import ensure_docker_compose_dir
    cwd = ensure_docker_compose_dir()

    service = service or get_default_service()

    #TODO: user

    call('docker exec -it %s /bin/bash' % service, shell=True)
