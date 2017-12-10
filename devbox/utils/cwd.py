import os

from typing import Optional


class CwdHelper:
    def __init__(self, cwd=os.getcwd()):
        self.__compose_dir = self.__get_compose_dir(cwd)
        self.__compose_file = self.__get_compose_file(self.__compose_dir)

    def get_compose_dir(self) -> str:
        return self.__compose_dir

    def get_compose_file(self) -> str:
        return self.__compose_file

    def get_compose_path(self) -> str:
        return self.__compose_dir + '/' + self.__compose_file

    def __get_compose_dir(self, cwd: str) -> str:
        if self.__get_compose_file(cwd):
            return cwd

        if os.path.isdir('docker'):
            cwd += '/docker'

            if (self.__get_compose_file(cwd)):
                return cwd

        raise FileNotFoundError(
            'Can\'t find a suitable configuration file in this directory or any parent. Are you in the right directory?')

    def __get_compose_file(self, path: str) -> Optional[str]:
        compose_files = ('docker-compose.yml', 'docker-compose.yaml')

        for compose_file in compose_files:
            if os.path.isfile(path + '/' + compose_file):
                return compose_file

        return None
