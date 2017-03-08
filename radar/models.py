from radar import db


__all__ = ['Commit']


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_hash = db.Column(db.String(40))
    summary = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    author = db.Column(db.String(100))
    commit_time = db.Column(db.DateTime)
    __table__args = (db.UniqueConstraint(commit_hash, branch))
