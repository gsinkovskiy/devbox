import click


@click.group(name='hosts')
def commands():
    pass


@commands.command(name='hosts:update')
@click.argument('container', nargs=-1)
def execute(container=None):
    """
    Update /etc/hosts file depends on current running containers
    """
    # print(container)
    click.echo('Update hosts')

    from devbox.utils import admin, docker as docker_utils
    import docker
    from python_hosts import Hosts, HostsEntry, utils
    from python_hosts.exception import UnableToWriteHosts

    #f = open('C:\\apps\\devbox\\a.txt', 'a')
    # f.write('1')
    # f.close()

    client = docker.from_env()
    # TODO: support containers
    containers = client.containers.list()
    hosts = Hosts()
    require_update = False

    for container in containers:
        # print(container.name)
        container_hosts = docker_utils.get_hosts(container)
        ip = docker_utils.get_ip(container)

        if (container_hosts):
            for container_host in container_hosts:
                hosts_entry = HostsEntry(
                    entry_type='ipv4', address=ip, names=[container_host])
                hosts.add([hosts_entry], force=True,
                          allow_address_duplication=True)
            require_update = True

    if (not require_update):
        click.echo('No hosts for update')
        return

    try:
        hosts.write()
    except UnableToWriteHosts:
        from sys import platform

        if platform.startswith('win'):
            if (not admin.is_admin()):
                click.echo(
                    'Unable update hosts file, retry again with admin roots.')
                admin.run_as_admin('devbox', ('hosts:update'))

            return

        from subprocess import call
        click.echo('Unable update hosts file, retry again with sudo.')
        call('sudo devbox hosts:update', shell=True)

    click.echo('Done')
