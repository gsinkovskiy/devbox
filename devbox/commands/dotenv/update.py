import click


@click.group(name='dotenv')
def commands():
    pass


@commands.command(name='dotenv:update')
def execute():
    """
    Update ".env" file based on ".env.dist" template
    """
    click.echo('Updating ".env" file based on ".env.dist" template')

    from ...utils.cwd import CwdHelper
    from ...utils.dotenv import DotenvHelper

    cwd = CwdHelper().get_compose_dir()
    dotenvHelper = DotenvHelper(cwd)

    if not dotenvHelper.exists(dotenvHelper.DOTENV_DIST_FILE):
        click.echo('"{dist_file}" does not exists.'.format(dist_file=dotenvHelper.DOTENV_DIST_FILE))

        return None

    requires_update = False
    current_envvars = dotenvHelper.parse(dotenvHelper.DOTENV_FILE)
    master_envvars = dotenvHelper.parse(dotenvHelper.DOTENV_DIST_FILE)
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

            if click.confirm('Remove "{variable}={value}"?'.format(variable=variable, value=value)):
                target_envvars.pop(variable)
                requires_update = True

    if not requires_update:
        click.echo('No any updates required.')
    else:
        click.echo('Writing new ".env" file.')
        dotenvHelper.dump(dotenvHelper.DOTENV_FILE, target_envvars)
