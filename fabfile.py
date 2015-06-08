from fabric.api import run, cd, env
from fabric.decorators import task


env.use_ssh_config = True
env.hosts = ['hackfourno5.cloudapp.net']


@task
def deploy_backend():
    with cd('/srv/www/AreaInfo'):
        run('git pull')
        run('venv/bin/pip install -r requirements.txt')
        run('cp area_info/static/* static')
        run('touch area_info/__init__.py')
