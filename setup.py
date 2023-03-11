"""Setup file for application"""
# To build: python -m build
# To check folder included: tar --list -f dist/bikerepair-1.0.tar.gz

from setuptools import setup, find_packages

setup(
    name='bikerepair',
    version='1.0',
    author='Sviatoslav Iliash',
    author_email='',
    description='Service for repair bicycles',
    long_description='Web service for clients who want to maintain their bicycles',
    url='https://github.com/SviatoslavIliash/EpamFinalProj',
    keywords='development, setup, setuptools',
    python_requires='>=3.9',
    packages=find_packages(include=['bikerepair', 'bikerepair.*', 'tests']),
    install_requires=[
        'alembic==1.10.2',
        'astroid==2.14.2',
        'attrs==22.2.0',
        'blinker==1.5',
        'build==0.10.0',
        'certifi==2022.12.7',
        'charset-normalizer==3.0.1',
        'click==8.1.3',
        'coverage==6.5.0',
        'coveralls==3.3.1',
        'dill==0.3.6',
        'docopt==0.6.2',
        'exceptiongroup==1.1.0',
        'Flask==2.2.2',
        'Flask-HTTPAuth==4.7.0',
        'Flask-Login==0.6.2',
        'Flask-Migrate==4.0.4',
        'Flask-SQLAlchemy==3.0.3',
        'greenlet==2.0.2',
        'gunicorn==20.1.0',
        'idna==3.4',
        'iniconfig==2.0.0',
        'isort==5.12.0',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'lazy-object-proxy==1.9.0',
        'Mako==1.2.4',
        'MarkupSafe==2.1.2',
        'mccabe==0.7.0',
        'mysql-connector-python==8.0.32',
        'packaging==23.0',
        'Pillow==9.4.0',
        'platformdirs==3.0.0',
        'pluggy==1.0.0',
        'protobuf==3.20.3',
        'pylint==2.16.2',
        'PyMySQL==1.0.2',
        'pyproject_hooks==1.0.0',
        'pytest==7.2.1',
        'pytest-mock==3.10.0',
        'PyYAML==6.0',
        'requests==2.28.2',
        'six==1.16.0',
        'SQLAlchemy==2.0.3',
        'tomli==2.0.1',
        'tomlkit==0.11.6',
        'typing_extensions==4.4.0',
        'urllib3==1.26.14',
        'Werkzeug==2.2.2',
        'wrapt==1.14.1',
        'yamlloader==1.2.2'
        ]
    )
