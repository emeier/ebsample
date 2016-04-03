import os

from contextlib import contextmanager

from fabric.api import task, local, prefix, env, execute

APP_NAME = 'sgdevops1'
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


@contextmanager
def activate_this():
    activate_this = os.path.join(VENV_PATH, 'bin', 'activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

    yield


@task
def dev():
    env.eb_env_name = APP_NAME + '-dev'
    env.eb_scale = 1


@task
def prod():
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
    execute(provision)


@task
def eb_init(name, platform='python2.7'):
    """
    Creates an Elastic Beanstalk application.
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
def eb_delete_app(name=None, force=False):
    if name is None:
        name = APP_NAME

    with activate_this():
        import boto3

        eb_client = boto3.client('elasticbeanstalk')

        response = eb_client.delete_application(
            ApplicationName=name,
            TerminateEnvByForce=force
        )

        print(response)


@task
def provision():
    """
    Creates the Elastic Beanstalk application and environment if it does not already exist.
    """
    with activate_this():
        import boto3

        eb_client = boto3.client('elasticbeanstalk')

        response = eb_client.describe_applications(
            ApplicationNames=[APP_NAME]
        )

        if APP_NAME in [a['ApplicationName'] for a in response['Applications']]:
            print(APP_NAME + ' exists, skipping creation.')
        else:
            print('Creating application: ' + APP_NAME)
            response = eb_client.create_application(
                ApplicationName=APP_NAME,
                Description=APP_DESCRIPTION
            )
            print(response)

        response = eb_client.describe_environments(
            ApplicationName=APP_NAME,
            EnvironmentNames=[env.eb_env_name]
        )
        print(response)
        if env.eb_env_name in [e['EnvironmentName'] for e in response['Environments']]:
            print(env.eb_env_name + ' exists, skipping creation.')
        else:
            print('Creating environment: ' + env.eb_env_name)
            response = eb_client.create_environment(
                ApplicationName=APP_NAME,
                EnvironmentName=env.eb_env_name,
                CNAMEPrefix=env.eb_env_name,
                SolutionStackName='python2.7'
            )
            print(response)
