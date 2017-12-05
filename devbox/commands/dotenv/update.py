import click


@click.group(name='dotenv')
def commands():
    pass


@commands.command(name='dotenv:update')
def execute():
    """
    Update .env file based on .env.dist template
    """

    click.echo('Updating .env file based on .env.dist template')

    from devbox.utils.dotenv import parse_dotenv, dump_dotenv
    from devbox.utils.cwd import ensure_docker_compose_dir
    import os

    ensure_docker_compose_dir()

    if not os.path.isfile('.env.dist'):
        click.echo('.env.dist does not exists.')

        return None

    requires_update = False
    current_envvars = parse_dotenv('.env')
    master_envvars = parse_dotenv('.env.dist')
    target_envvars = current_envvars.copy()

    displayed_notice = False
    for variable, value in master_envvars.items():
        if variable not in current_envvars:
            if not displayed_notice:
                click.echo('There are some new variables:')
                displayed_notice = True

            new_value = click.prompt(variable + '=', default=value, type=str)
            target_envvars.update({variable: new_value})
            requires_update = True

    displayed_notice = False
    for variable, value in current_envvars.items():
        if variable not in master_envvars:
            if not displayed_notice:
                click.echo('Some variables are missing:')
                displayed_notice = True

            if click.confirm('Remove "{0}={1}"?'.format(variable, value)):
                target_envvars.pop(variable)
                requires_update = True

    if not requires_update:
        click.echo('No any updates required.')
    else:
        click.echo('Writing new .env.')
        dump_dotenv(target_envvars, '.env')
