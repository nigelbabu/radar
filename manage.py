#!/usr/bin/env python

from flask_script import Server, Manager
from radar import app, db
from radar.models import Commit
from radar.cli import get_repo
from datetime import datetime
from pytz import timezone


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

    url = repos[name].get('url')
    branches = repos[name].get('branches', ['master'])
    repo = get_repo(url, name)
    repo.remote().update()
    tz = timezone('US/Pacific')
    for branch in branches:
        print branch
        repo.git.checkout(branch)
        repo.remote().pull(branch)
        for commit in repo.iter_commits(branch, max_count=10):
            change = Commit.query.filter_by(
                    commit_hash=commit.hexsha,
                    branch=branch
            ).first()
            if not change:
                change = Commit(
                        commit_hash=commit.hexsha,
                        summary=commit.summary,
                        branch=branch,
                        author=u"{} <{}>".format(commit.author.name, commit.author.email),
                        commit_time=commit.committed_datetime,
                )
                db.session.add(change)
                db.session.commit()




if __name__ == '__main__':
    manager.run()
