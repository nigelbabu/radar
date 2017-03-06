from radar import db


__all__ = ['Commit']


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_hash = db.Column(db.DateTime)
    summary = db.Column(db.String(100))
    branch = db.Column(db.String(50))
    author = db.Column(db.String(100))
    commit_time = db.Column(db.String(40))
