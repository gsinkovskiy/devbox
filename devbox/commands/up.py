import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='up', context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
@click.argument('service', required=False)
# @click.option('compose_args', type=click.UNPROCESSED)
@click.argument('compose_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def execute(ctx, compose_args, service=None):
    """
    Up Docker containers depends on docker-compose.yaml file.

      - up the containers

      - fix Docker for Windows specific bugs

      - updates /etc/hosts depends for container IPs
    """
    from subprocess import call
    # TODO: allow start single container
    # TODO: handle not daemon mode

    from devbox.utils.cwd import CwdHelper
    from devbox.utils import WIN
    cwd = CwdHelper().get_compose_dir()

    from devbox.commands.dotenv.update import execute as update_dotenv
    ctx.invoke(update_dotenv)

    click.echo('Starting docker containers')
    cmdline = ['docker-compose', 'up', '-d'] + list(compose_args)
    click.echo('Invoking: %s' % ' '.join(cmdline))
    retcode = call(cmdline, cwd=cwd)

    if retcode > 0:
        click.echo('En error occurred during docker-compose. Stop execution.')

        return None

    click.echo('Done.')

    if WIN:
        from devbox.commands.fix import execute as fix
        ctx.invoke(fix)

    from devbox.commands.hosts.update import execute as update_hosts
    ctx.invoke(update_hosts)
