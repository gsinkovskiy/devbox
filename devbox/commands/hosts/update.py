import click


@click.group(name='hosts')
def commands():
    pass


@commands.command(name='hosts:update')
@click.argument('containers', nargs=-1)
def execute(containers=None):
    """
    Update "/etc/hosts" file depends on current running containers.
    """
    # print(container)
    click.echo('Update hosts')

    from devbox.utils import admin
    from devbox.utils.docker import DockerHelper, get_hosts, get_ip
    from python_hosts import Hosts, HostsEntry
    from python_hosts.exception import UnableToWriteHosts
    from devbox.utils import WIN

    # f = open('C:\\apps\\devbox\\a.txt', 'a')
    # f.write('1')
    # f.close()

    docker_helper = DockerHelper()
    runned_containers = docker_helper.get_containers()
    if (not containers):
        containers = [container.name for container in runned_containers]

    hosts = Hosts()
    require_update = False

    for container in runned_containers:
        if not container.name in containers:
            continue

        container_hosts = get_hosts(container)
        ip = get_ip(container)
        if not ip:
            click.echo('Container "{0}" has not ip'.format(container.name))

        if container_hosts:
            for container_host in container_hosts:
                hosts_entry = HostsEntry(entry_type='ipv4', address=ip, names=[container_host])
                hosts.add([hosts_entry], force=True, allow_address_duplication=True)
            require_update = True

    if not require_update:
        click.echo('No hosts for update')
        return

    try:
        hosts.write()
    except UnableToWriteHosts:
        # TODO: pass containers
        if WIN:
            if not admin.is_admin():
                click.echo(
                    'Unable update hosts file, retry again with admin roots.')
                admin.run_as_admin('devbox', 'hosts:update')

            return

        from subprocess import call
        click.echo('Unable update hosts file, retry again with sudo.')
        call('sudo devbox hosts:update', shell=True)

    click.echo('Done')
