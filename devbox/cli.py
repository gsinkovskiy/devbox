import importlib

import click


@click.group(name='main')
def cli():
    pass


# @click.group(name='main', invoke_without_command=True, no_args_is_help=True)
# @click.pass_context
# def cli(ctx):
#     if ctx.invoked_subcommand is None:
#         click.echo('I was invoked without subcommand')
#     else:
#         click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


commands = ['bash', 'dockerfile.generate', 'devbox.update', 'down', 'dotenv.update', 'hosts.update', 'fix',
            'ssh', 'up']

for command in commands:
    # module = __import__('commands.'+command, fromlist=['execute'])
    # cli.add_command(getattr(module, 'execute'))

    module = importlib.import_module('.commands.' + command, package='devbox')
    cli.add_command(getattr(module, 'execute'))

if __name__ == '__main__':
    cli()
