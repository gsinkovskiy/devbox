from typing import Optional, List

from docker.models.containers import Container


class DockerHelper:
    def __init__(self):
        import docker

        self.client = docker.from_env()
        pass

    def get_client(self):
        return self.client

    def get_full_volume_name(self, name: str) -> Optional[str]:
        for volume in self.client.volumes.list():
            if not volume.attrs['Labels']:
                continue

            if volume.attrs['Labels']['com.docker.compose.volume'] == name:
                return volume.attrs['Name']

        return None

    def get_used_containers_for_volume(self, volume_name: str) -> List[Container]:
        used_containers = list()
        for container in self.client.containers.list(all=True):
            for mount in container.attrs['Mounts']:
                if not 'Name' in mount:
                    continue

                if mount['Name'] == volume_name:
                    used_containers.append(container)

        return used_containers


def get_env(container, key: str) -> Optional[str]:
    envs = container.attrs['Config']['Env']
    for env_item in envs:
        variable, value = env_item.split('=', 1)
        if variable == key:
            return value

    return None


def get_ip(container: Container) -> Optional[str]:
    for network_name, network in container.attrs['NetworkSettings']['Networks'].items():
        ip = network['IPAddress']
        if ip:
            return ip
    return None


def get_hosts(container: Container) -> List[str]:
    container_hosts = [container.name]

    expose_hosts = get_env(container, 'EXPOSE_HOSTS')
    if expose_hosts:
        container_hosts.extend(
            [host for host in expose_hosts.split("\n") if host])

    from python_hosts import utils

    container_hosts = utils.dedupe_list(container_hosts)

    return container_hosts


def get_default_service() -> Optional[str]:
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
