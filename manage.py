#!/usr/bin/env python

from flask_script import Server, Manager
from radar import app, db
from radar.cli import clone_or_update_repo


manager = Manager(app)
manager.add_command('runserver', Server())


@manager.command
def db_init():
    db.create_all()


@manager.option('-r', '--repo', dest='name', required=True)
def update_repo(name):
    repos = app.config.get('GIT_REPOS')
    if name not in repos:
        raise Exception('Repository not found')
    url = repos[name]
    clone_or_update_repo(url, name)


if __name__ == '__main__':
    manager.run()
