#!/usr/bin/env python

from flask_script import Server, Manager
from radar import app, db
from radar.models import Commit
from radar.cli import get_repo
from datetime import datetime


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
    for branch in branches:
        repo.git.checkout(branch)
        repo.remote().pull(branch)
        # Get the last 10 commits if there are no entries for this branch
        rev = "HEAD~10...HEAD"
        # Find the latest commit for each branch
        latest = Commit.query.filter_by(branch=branch
                ).order_by(Commit.commit_time.desc()).first()
        if latest:
            rev = "HEAD...{}".format(latest.commit_hash)

        for commit in repo.iter_commits(rev):
            # Check if the commit exists before creating a new entry
            change = Commit.query.filter_by(
                    commit_hash=commit.hexsha,
                    branch=branch
            ).first()
            if not change:
                change = Commit(
                        commit_hash=commit.hexsha,
                        summary=commit.summary,
                        branch=branch,
                        author=u"{} <{}>".format(
                            commit.author.name,
                            commit.author.email
                        ),
                        commit_time=commit.committed_datetime,
                )
                db.session.add(change)
                db.session.commit()




if __name__ == '__main__':
    manager.run()
