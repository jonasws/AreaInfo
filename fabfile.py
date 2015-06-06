from fabric.api import run, cd, env


env.use_ssh_config = True

env.hosts = ['hackfourno5.cloudapp.net']

def deploy_backend():
    with cd('/srv/www/AreaInfo'):
        run('git pull')
        run('venv/bin/pip install -r requirements.txt')
        run('touch app.py')
