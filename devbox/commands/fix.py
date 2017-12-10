import click


@click.group(name='main')
def commands():
    pass


@commands.command(name='fix')
@click.pass_context
def execute(ctx):
    """
    Fix Docker for Windows specific bugs.

    For now it fixes network access to containers by internal ip (172.x.x.x).
    """
    from subprocess import call

    click.echo('Fix iptables')
    cmd = 'docker run --rm -ti --privileged --network=none --pid=host justincormack/nsenter1 bin/sh -c "iptables -A FORWARD -j ACCEPT"'
    call(cmd)
    click.echo('Done')

    from .routes.update import execute as update_routes
    ctx.invoke(update_routes)
