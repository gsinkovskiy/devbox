import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='down', context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
@click.argument('service', required=False)
# @click.option('compose_args', type=click.UNPROCESSED)
@click.argument('compose_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def execute(ctx, compose_args, service=None):
    """
    Down docker containers depends on docker-compose.yaml file

      - stop the containers

      - updates /etc/hosts depends for container IPs
    """
    from subprocess import call
    # TODO: allow stop single container

    from ..utils.cwd import CwdHelper
    cwd = CwdHelper().get_compose_dir()

    click.echo('Restore hosts')
    from .hosts.update import execute as update_hosts
    ctx.invoke(update_hosts)
    click.echo('Done')

    click.echo('Stopping containers')
    cmdline = ['docker-compose', 'down'] + list(compose_args)
    click.echo('Invoking: %s' % ' '.join(cmdline))
    call(cmdline, cwd=cwd)
    click.echo('Done')
