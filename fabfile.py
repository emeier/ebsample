import os

from contextlib import contextmanager

from fabric.api import task, local, prefix

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
VENV_PATH = os.path.join(CURRENT_PATH, 'venv')
VENV_ACTIVATE_PATH = os.path.join(VENV_PATH, 'bin', 'activate')
REQ_PATH = os.path.join(CURRENT_PATH, 'requirements.txt')


@contextmanager
def virtualenv():
    if not os.path.exists(VENV_PATH):
        local('virtualenv --no-site-packages {0}'.format(VENV_PATH))

    with prefix('source {0}'.format(VENV_ACTIVATE_PATH)):
        yield


@task
def install():
    """
    Creates a development virtualenv and pip installs requirements
    """

    with virtualenv():
        local('pip install -r {0}'.format(REQ_PATH))


@task
def server():
    """
    Starts the development web server
    """
    app_path = os.path.join(CURRENT_PATH, 'application.py')

    with virtualenv():
        local('python {0}'.format(app_path))


@task
def eb_init(name, platform='python2.7'):
    """
    Creates an elastic beanstalk application.
    """
    with virtualenv():
        local('eb init -p {0} {1}'.format(platform, name))


@task
def eb_create_env(name=None):
    cmd = 'eb create'

    if name is not None:
        cmd += ' ' + name

    local(cmd)


@task
def eb_list():
    """
    Lists all Elastic Beanstalk environments
    """
    with virtualenv():
        local('eb list')


@task
def eb_deploy():
    """
    Deploys to an Elastic Beanstalk environment
    """
    with virtualenv():
        local('eb deploy')


@task
def eb_terminate(name):
    """
    Terminates an Elastic Beanstalk environment
    """
    with virtualenv():
        local('eb terminate {0}'.format(name))


@task
def eb_scale(number, name=None):
    """
    Changes the number of running instances
    """
    cmd = 'eb scale {0}'.format(number)

    if name is not None:
        cmd += ' ' + name

    with virtualenv():
        local(cmd)
