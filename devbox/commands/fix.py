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
    call(
        'docker run --rm -ti --privileged --network=none --pid=host justincormack/nsenter1 bin/sh -c "iptables -A FORWARD -j ACCEPT"')
    click.echo('Done')

    from devbox.commands.routes.update import execute as update_routes
    ctx.invoke(update_routes)
