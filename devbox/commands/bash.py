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
    from ..utils.docker import get_default_service
    from ..utils.cwd import CwdHelper

    if not service:
        service = get_default_service(CwdHelper().get_compose_path())

    # TODO: change user

    cmd = 'docker exec -it {0} /bin/bash'.format(service)
    call(cmd, shell=True)
