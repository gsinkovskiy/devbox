import click
import importlib

@click.group()
def cli():
    pass

commands = ['up', 'bash', 'ssh', 'hosts.update', 'devbox.update']

for command in commands:
    #module = __import__('commands.'+command, fromlist=['execute'])
    #cli.add_command(getattr(module, 'execute'))

    module = importlib.import_module('.commands.'+command, package='devbox')
    cli.add_command(getattr(module, 'execute'))

if __name__ == '__main__':
    cli()
