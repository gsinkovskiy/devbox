from collections import OrderedDict
import os


def parse_dotenv(path):
    envvars = OrderedDict()
    if (os.path.isfile(path)):
        for line in open(path).readlines():
            variable, value = line.split('=', 1)
            envvars.update({variable: value.rstrip()})
            # envvars.move_to_end(variable)

    return envvars


def dump_dotenv(envvars: OrderedDict, path):
    with open(path, 'w') as file:
        for variable, value in envvars.items():
            file.write('{0}={1}\n'.format(variable, value))

    file.close()
