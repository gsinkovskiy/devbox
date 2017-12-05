import click


@click.group(name='dockerfile')
def commands():
    pass


@commands.command(name='dockerfile:generate')
def execute(template='Dockerfile.jinja2', settings_file='.devbox.build.yaml'):
    """
    Generates Dockerfile's from given template
    """
    # print(container)
    click.echo('Generate Dockerfile\'s')

    import os

    if not os.path.isfile(template):
        click.echo('No template "{0}" exists in current folder'.format(template))

        return None

    if not os.path.isfile(settings_file):
        click.echo('No settings file "{0}" exists in current folder'.format(settings_file))

        return None

    from jinja2 import Template
    content = open(template).read()
    jinja_template = Template(content)

    import yaml

    with open(settings_file, 'r') as stream:
        try:
            settings = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

            raise exc

        context = dict()
        if 'context' in settings:
            context = settings['context']

        if 'builds' in settings:
            for build in settings['builds']:
                context['BUILD'] = build

                if not os.path.isfile(build + '/' + settings_file):
                    click.echo('No settings file "{0}" exists for build {1}'.format(settings_file, build))
                else:
                    with open(build + '/' + settings_file, 'r') as stream:
                        try:
                            build_settings = yaml.load(stream)
                        except yaml.YAMLError as exc:
                            print(exc)

                            raise exc

                        if 'context' in build_settings:
                            context = {**context, **build_settings['context']}

                output = jinja_template.render(context)

                # print(output)

                dockerfile_path = build + '/' + 'Dockerfile'
                with open(dockerfile_path, 'w') as output_dockerfile:
                    click.echo('Writing compiled Dockerfile "{0}"'.format(dockerfile_path))
                    output_dockerfile.write(output+'\n')
                    output_dockerfile.close()
