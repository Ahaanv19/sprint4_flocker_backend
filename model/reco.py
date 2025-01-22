from __init__ import db

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    def read(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre
        }

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self