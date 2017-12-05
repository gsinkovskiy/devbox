import click


@click.group(name='dockerfile')
def commands():
    pass


@commands.command(name='dockerfile:generate')
def execute(template='Dockerfile.jinja2', settings_file='.devbox.build.yaml'):
    """
    Generates Dockerfile's from given template
    """
    click.echo('Generate Dockerfile\'s')

    import os

    if not os.path.isfile(template):
        click.echo('Template "{0}" not found in current folder. Cannot build.'.format(template))

        raise None

    if not os.path.isfile(settings_file):
        click.echo('Settings file "{0}" found in current folder. Cannot build.'.format(settings_file))

        return None

    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True, lstrip_blocks=True,
                      keep_trailing_newline=True)
    jinja_template = env.get_template(template)

    import yaml

    with open(settings_file, 'r') as stream:
        try:
            settings = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

            raise exc

        vars = dict()
        if 'vars' in settings:
            vars = settings['vars']

        if not 'builds' in settings:
            click.echo('Settings file "{0}" does not contains "builds" section.'.format(settings_file))

            return None

        for build in settings['builds']:
            vars['BUILD'] = build

            if not os.path.isfile(build + '/' + settings_file):
                click.echo('No settings file "{0}" found for build "{1}".'.format(settings_file, build))
            else:
                with open(build + '/' + settings_file, 'r') as stream:
                    try:
                        build_settings = yaml.load(stream)
                    except yaml.YAMLError as exc:
                        print(exc)

                        raise exc

                    if 'vars' in build_settings:
                        vars = {**vars, **build_settings['vars']}

            output = jinja_template.render(vars)

            dockerfile_path = build + '/' + 'Dockerfile'
            if 'dockerfile' in build_settings:
                dockerfile_path = build_settings['dockerfile']

            with open(dockerfile_path, 'w') as output_dockerfile:
                click.echo('Writing compiled Dockerfile "{0}".'.format(dockerfile_path))
                output_dockerfile.write(output)
                output_dockerfile.close()
