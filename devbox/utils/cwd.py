import os

def ensure_docker_compose_dir():
    cwd = os.getcwd()

    if (docker_compose_exists()):
        return os.getcwd()

    if (os.path.isdir('docker')):
        os.chdir('docker')

        if (docker_compose_exists()):
            return os.getcwd()

    # TODO: handle parent paths?
    os.chdir(cwd)

    raise FileNotFoundError(
        'Can\'t find a suitable configuration file in this directory or any parent. Are you in the right directory?')


def docker_compose_exists():
    files = ('docker-compose.yml', 'docker-compose.yaml')

    for file in files:
        if (os.path.isfile(file)):
            return True

    return False
