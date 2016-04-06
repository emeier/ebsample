import os

from contextlib import contextmanager
from distutils.util import strtobool

from fabric.api import task, local, prefix, env, settings

APP_NAME = 'sgdevops'
APP_DESCRIPTION = """
A sample application for use with Elastic Beanstalk
"""
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
USER_HOME = os.path.expanduser('~')
VENV_PATH = os.path.join(USER_HOME, 'venv')


@contextmanager
def virtualenv():
    if not os.path.exists(VENV_PATH):
        local('virtualenv --no-site-packages {0}'.format(VENV_PATH))

    activate = os.path.join(VENV_PATH, 'bin', 'activate')
    with prefix('source {0}'.format(activate)):
        yield


@task
def dev():
    """
    Sets the dev env vars
    """
    env.eb_env_name = APP_NAME + '-dev'
    env.eb_scale = 1
    env.eb_instance_type = 't2.micro'


@task
def prod():
    """
    Sets the prod env vars
    """
    env.eb_env_name = APP_NAME + '-prod'
    env.eb_scale = 2
    env.eb_instance_type = 'm4.large'


@task
def install(clean='n'):
    """
    Creates a development virtualenv and pip installs requirements
    """
    if strtobool(clean):
        local('rm -rf {0}'.format(VENV_PATH))

    requirements = os.path.join(CURRENT_PATH, 'requirements.txt')

    with virtualenv():
        local('pip install -U setuptools==20.6.7')
        local('pip install -U pip==8.1.1')
        local('pip install -r {0}'.format(requirements))


@task
def server():
    """
    Starts the development web server
    """
    app_path = os.path.join(CURRENT_PATH, 'application.py')

    with virtualenv():
        local('python {0}'.format(app_path))


@task
def deploy():
    """
    Deploys to Elastic Beanstalk, creating the environment if it does not exist.
    """
    eb_init(APP_NAME)

    with settings(warn_only=True):
        status = eb_status(env.eb_env_name)

    if status.failed:
        eb_create(env.eb_env_name, instance_type=env.eb_instance_type, scale=env.eb_scale)
    else:
        eb_deploy(env.eb_env_name)


@task
def terminate():
    """
    Terminates an Elastic Beanstalk environment
    """
    eb_terminate(env.eb_env_name)


@task
def eb_init(name, platform='python2.7', region='us-west-2'):
    """
    Creates an Elastic Beanstalk application.
    """
    with virtualenv():
        local('eb init {0} -p {1} -r {2}'.format(name, platform, region))


@task
def eb_create(name, cname=None, instance_type='t2.micro', scale=1):
    """
    Creates a new Elastic Beanstalk environment.

    Throws an exception if the environment already exists.
    """
    if cname is None:
        cname = name

    cmd = 'eb create {0} --cname {1} -i {2} --scale {3}'.format(
        name, cname, instance_type, scale
    )

    with virtualenv():
        local(cmd)


@task
def eb_list():
    """
    Lists all Elastic Beanstalk environments
    """
    with virtualenv():
        local('eb list')


@task
def eb_status(name):
    """
    Gets Elastic Beanstalk environment information and status
    """

    cmd = 'eb status {0}'.format(name)

    with virtualenv():
        result = local(cmd, capture=True)

    return result


@task
def eb_deploy(name):
    """
    Deploys to an Elastic Beanstalk environment
    """

    cmd = 'eb deploy {0}'.format(name)

    with virtualenv():
        local(cmd)


@task
def eb_terminate(name):
    """
    Terminates an Elastic Beanstalk environment
    """
    with virtualenv():
        local('eb terminate {0} --force'.format(name))


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


@task
def config():
    """
    Edits the Elastic Beanstalk environment configuration settings
    """
    cmd = 'eb config {0}'.format(env.eb_env_name)

    with virtualenv():
        local(cmd)


@task
def health():
    """
    Shows detailed environment health
    """
    cmd = 'eb health {0}'.format(env.eb_env_name)

    with virtualenv():
        local(cmd)
