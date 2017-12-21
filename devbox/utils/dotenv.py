import os
from collections import OrderedDict
from typing import Optional


class DotenvHelper:
    __slots__ = ('__base_dir')

    DOTENV_DIST_FILE = '.env.dist'
    DOTENV_FILE = '.env'

    def __init__(self, cwd: str = os.getcwd()):
        self.__base_dir = cwd
        pass

    def exists(self, path: str) -> bool:
        path = self.__normalize_path(path)

        return os.path.exists(path)

    def parse(self, path: str) -> OrderedDict:
        path = self.__normalize_path(path)

        envvars = OrderedDict()
        if os.path.isfile(path):
            for line in open(path).readlines():
                variable, value = line.split('=', 1)
                envvars.update({variable: value.rstrip()})
                # envvars.move_to_end(variable)

        return envvars

    def dump(self, path: str, envvars: OrderedDict):
        path = self.__normalize_path(path)

        with open(path, 'w') as file:
            for variable, value in envvars.items():
                file.write('{variable}={value}\n'.format(variable=variable, value=value))

        file.close()

    def get_env(self, key: str) -> Optional[str]:
        if self.exists(self.DOTENV_DIST_FILE):
            envvars = self.parse(self.DOTENV_FILE)
            if key in envvars:
                return envvars.get(key)

        return None

    def __normalize_path(self, path: str) -> str:
        if not os.path.isabs(path):
            path = self.__base_dir + '/' + path
        return path
