#!/usr/bin/env python
from __future__ import unicode_literals
import io
import os
from fabric.api import *

@task
def iptables():
    put('iptables.sh', 'iptables.sh', mode=0o700)
    run('./iptables.sh')

@task
def create_bot_user():
    run('useradd bot', warn_only=True)


@task
def put_bot():
    run('mkdir -p /var/bot')
    with cd('/var/bot'):
        run('rm -rf botenv')
        run('virtualenv botenv --system-site-packages -p `which python3`')

        put('bot.py', '/var/bot/bot.py')
        put('bot.sh', '/var/bot/bot.sh', mode=0o500,)
        put('crontab', '/var/bot/crontab')
        put('freeze.txt', '/var/bot/freeze.txt')

        fp = io.StringIO()
        fp.write('''\
#!/bin/sh
export TWITTER_BOT_APP_KEY='{}'
export TWITTER_BOT_APP_SECRET='{}'
export TWITTER_BOT_OAUTH_TOKEN='{}'
export TWITTER_BOT_OAUTH_TOKEN_SECRET='{}'
'''.format(
            os.environ['TWITTER_BOT_APP_KEY'],
            os.environ['TWITTER_BOT_APP_SECRET'],
            os.environ['TWITTER_BOT_OAUTH_TOKEN'],
            os.environ['TWITTER_BOT_OAUTH_TOKEN_SECRET'],
        ))
        put(fp, '/var/bot/init.sh')

        run('botenv/bin/pip install -r freeze.txt')
        run('chown -R bot:bot /var/bot')
        run('crontab -u bot crontab')


@task
def restart_services():
    run('service cron restart')

@task
def install_postfix():
    run('debconf-set-selections <<< "postfix postfix/mailname string `hostname`"')
    run('''debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"''')
    run('apt-get install -y postfix')


@task
def setup():
    run('apt-get install -y python-pip python3-lxml iptables')
    install_postfix()
    iptables()
    run('pip install virtualenv')
    create_bot_user()
    put_bot()
    restart_services()

