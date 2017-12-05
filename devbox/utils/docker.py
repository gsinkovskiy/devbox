def get_env(container, key: str):
    envs = container.attrs['Config']['Env']
    for env_item in envs:
        variable, value = env_item.split('=', 1)
        if variable == key:
            return value

    return None


def get_ip(container):
    for network_name, network in container.attrs['NetworkSettings']['Networks'].items():
        ip = network['IPAddress']
        if ip:
            return ip
    else:
        print('Container "%s" has not ip' % container.name)
        return None


def get_hosts(container):
    container_hosts = [container.name]

    expose_hosts = get_env(container, 'EXPOSE_HOSTS')
    if expose_hosts:
        container_hosts.extend(
            [host for host in expose_hosts.split("\n") if host])

    from python_hosts import utils

    container_hosts = utils.dedupe_list(container_hosts)

    return container_hosts


def get_default_service():
    import yaml
    import yamlordereddictloader
    import os

    files = ('docker-compose.yml', 'docker-compose.yaml')

    for file in files:
        if os.path.isfile(file):
            break
    else:
        return None

    with open(file, 'r') as stream:
        try:
            doc = yaml.load(stream, Loader=yamlordereddictloader.Loader)
        except yaml.YAMLError as exc:
            print(exc)

            raise exc

        if 'services' in doc:
            for service in doc['services']:
                service_config = doc['services'].get(service)

                return service_config.get('container_name') or service

    return None
