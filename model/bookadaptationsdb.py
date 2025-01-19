from __init__ import app, db
import logging

# Renaming the class to 'Book' (singular) and capitalizing it
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    
    def __init__(self, title):
        self.title = title

    def create(self):
        """Create a new book entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating book: {str(e)}")
            return None
        return self
        
    def delete(self):
        """Delete a book entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting book: {str(e)}")
            raise e
    
    def serialize(self):
        """Serialize the book object to a dictionary."""
        return {
            'id': self.id,
            'title': self.title
        }

def initBookAdaptations():
    # Check if any books exist in the database
    if not Book.query.first():
        # Create a list of books to be added
        book_list = [
            Book(title="The Great Gatsby"), 
            Book(title="1984"),
            Book(title="To Kill a Mockingbird"),
            Book(title="Harry Potter and the Sorcerer's Stone"),
            Book(title="Where the Red Fern Grows"),
            Book(title="A Wrinkle in Time")
        ]
        
        # Add each book to the database
        for book in book_list:
            book.create()
        print("Books added to the database.")
    else:
        print("Books already exist in the database.")
