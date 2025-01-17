from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
from sqlite3 import IntegrityError
from sqlalchemy import inspect


class NewBook(db.Model):
    __tablename__ = 'newBook'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    
    def __init__(self, id, title):
       
        self.id = id
        self.title = title
        
    def __repr__(self):

        return f"<BookCreation(id={self.id}, title='{self.title}>"


    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error creating book: {str(e)}")

    def read(self):
        return {
            'id': self.id,
            'title': self.title
        }

    def update(self, data):
        """
        Updates the quiz with new data and commits the changes.
        """
        if not self:
            raise ValueError("Quiz does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error updating quiz: {str(e)}")
        
    def delete(self):
        if not self:
            raise ValueError("Book does not exist.")
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error deleting book: {str(e)}")
    
   
    @staticmethod
    def restore(data):
        """
        Restores the books from the given data. It either updates existing books based on their ID
        or creates new books if they don't exist.
        
        Args:
            data (list): A list of dictionaries containing book data to restore.
            
        Returns:
            dict: A dictionary with 'id' as key and 'NewBook' object as value for all restored books.
        """
        books = {}
        for book_data in data:
            book_data.pop('id', None)

            book_id = book_data.get('id', None)
            
            if book_id is None:
                continue  

            book = NewBook.query.filter_by(id=book_id).first()

            if book:
                book.update(book_data)
            else:
                book = NewBook(**book_data)
                book.create()

            books[book_id] = book

        return books

        
def initBookAdaptations():
    with app.app_context():
        db.create_all()  # Create all tables
        inspector = inspect(db.engine)
        print(f"Tables created: {inspector.get_table_names()}")

        # Sample test data
        books = [
            NewBook(title="The Great Gatsby", id=1),
            NewBook(title="1984", id=2),
            NewBook(title="To Kill a Mockingbird", id=3)
        ]
        for book in books:
            try:
                book.create()
                print(f"Created book: {book}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {book.title}")

