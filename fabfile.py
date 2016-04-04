import os

from contextlib import contextmanager

from fabric.api import task, local, prefix, env, settings

APP_NAME = 'sgdevops'
APP_DESCRIPTION = """
A sample application for use with Elastic Beanstalk
"""
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
VENV_PATH = os.path.join(CURRENT_PATH, 'venv')


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


@task
def prod():
    """
    Sets the prod env vars
    """
    env.eb_env_name = APP_NAME + '-prod'
    env.eb_scale = 2


@task
def install():
    """
    Creates a development virtualenv and pip installs requirements
    """
    requirements = os.path.join(CURRENT_PATH, 'requirements.txt')

    with virtualenv():
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
        eb_create(env.eb_env_name)
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
def eb_create(name, cname=None):
    """
    Creates a new Elastic Beanstalk environment.

    Throws an exception if the environment already exists.
    """
    if cname is None:
        cname = name

    cmd = 'eb create {0} --cname {1}'.format(name, cname)

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

    cmd = 'eb deploy {0} -v'.format(name)

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
