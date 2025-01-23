from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)

def add_book_to_db(book_data):
    new_book = Book(
        title=book_data['title'],
        author=book_data['author'],
        genre=book_data['genre']
    )
    db.session.add(new_book)
    db.session.commit()
    return new_book