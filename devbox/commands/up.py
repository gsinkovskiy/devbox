import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='up', context_settings=dict(
    ignore_unknown_options=True,
    allow_interspersed_args=False
))
@click.argument('service', required=False)
#@click.option('compose_args', type=click.UNPROCESSED)
@click.argument('compose_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def execute(ctx, compose_args, service=None):
    """
    Up docker containers depends on docker-compose.yaml file
    """
    import sys
    from subprocess import call
    # TODO: allow start single container
    # TODO: handle not daemon mode
    # TODO: add network route

    from var_dump import var_dump
    from devbox.utils.cwd import ensure_docker_compose_dir
    cwd = ensure_docker_compose_dir()

    cmdline = ['docker-compose', 'up', '-d'] + list(compose_args)
    click.echo('Invoking: %s' % ' '.join(cmdline))

    call(cmdline, cwd=cwd)
    click.echo('Done')

    click.echo('Fix iptables')
    call('docker run --rm -ti --privileged --network=none --pid=host justincormack/nsenter1 bin/sh -c "iptables -A FORWARD -j ACCEPT"')
    click.echo('Done')

    click.echo('Update hosts')
    from devbox.commands.hosts.update import execute as update_hosts
    ctx.invoke(update_hosts)
    click.echo('Done')

# devbox up
#   up containers
#   update hosts
#   add network route
