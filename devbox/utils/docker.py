from typing import Optional, List

from docker import DockerClient
from docker.models.containers import Container
from docker.models.volumes import Volume


class DockerHelper:
    def __init__(self):
        import docker

        self.client = docker.from_env()
        pass

    def get_client(self) -> DockerClient:
        return self.client

    def get_full_volume_name(self, volume_name: str, compose_project: str) -> Optional[str]:
        for volume in self.client.volumes.list():
            if not volume.attrs['Labels']:
                continue

            labels = volume.attrs['Labels']
            if labels['com.docker.compose.volume'] == volume_name \
                    and labels['com.docker.compose.project'] == compose_project:
                return volume.attrs['Name']

        return None

    def get_volume(self, full_volume_name: str) -> Volume:
        return self.client.volumes.get(full_volume_name)

    def get_used_containers_for_volume(self, volume_name: str) -> List[Container]:
        used_containers = list()
        for container in self.get_containers(all=True):
            for mount in container.attrs['Mounts']:
                if not 'Name' in mount:
                    continue

                if mount['Name'] == volume_name:
                    used_containers.append(container)

        return used_containers

    def get_container(self, container_id: str) -> Container:
        return self.client.containers.get(container_id)

    def get_containers(self, all=False, before=None, filters=None, limit=-1, since=None) -> List[Container]:
        return self.client.containers.list(all, before, filters, limit, since)


def get_compose_project_name() -> Optional[str]:
    from ..utils.cwd import CwdHelper
    from ..utils.dotenv import DotenvHelper

    try:
        cwd = CwdHelper().get_compose_dir()
    except FileNotFoundError:
        return None

    compose_project = DotenvHelper(cwd).get_env('COMPOSE_PROJECT_NAME')

    return compose_project.replace('-', '')


def get_env(container: Container, key: str) -> Optional[str]:
    envvars = container.attrs['Config']['Env']
    for line in envvars:
        variable, value = line.split('=', 1)
        if variable == key:
            return value

    return None


def get_workdir(container: Container) -> str:
    return container.attrs['Config']['WorkingDir']


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
        container_hosts.extend([host for host in expose_hosts.split("\n") if host])

    from python_hosts import utils

    container_hosts = utils.dedupe_list(container_hosts)

    return container_hosts


def get_default_service(compose_path: str) -> Optional[str]:
    import yaml
    import yamlordereddictloader

    with open(compose_path, 'r') as stream:
        try:
            compose_config = yaml.load(stream, Loader=yamlordereddictloader.Loader)
        except yaml.YAMLError as exc:
            print(exc)

            raise exc

        if 'services' in compose_config:
            for service in compose_config['services']:
                service_config = compose_config['services'].get(service)

                return service_config.get('container_name') or service

    return None
