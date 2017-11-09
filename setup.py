from setuptools import setup

setup(
    name='devbox',
    version='0.1',
    py_modules=['devbox'],
    packages=['devbox'],
    package_dir={'devbox': 'devbox'},
    include_package_data=True,
    install_requires=[
        'click>=6.7',
        'docker>=2.5.1',
        'python-hosts>=0.4.1',
        'PyYAML>=3.12',
    ],
    entry_points='''
        [console_scripts]
        devbox=devbox.cli:cli
    ''',
)
