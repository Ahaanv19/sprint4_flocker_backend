from __init__ import app, db
import logging
class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    
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
    
    def read(self):
        """
        Returns the book details as a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title
        }
    
    def update(self, data):
        """
        Updates the book with new data and commits the changes.
        """
        if not self:
            raise ValueError("Book does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating book: {str(e)}")
            raise e
    
    def delete(self):
        """Delete a book entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting book: {str(e)}")
            raise e
    
def initbooking():
    # Check if any books exist in the database
    if not Booking.query.first():
        # Create a list of books to be added
        book_list = [
            Booking(title="Noah's Great Demise"), 
            Booking(title="18 Days of School"),
            Booking(title="To Kill a Mockingbird"),
            Booking(title="Harry Potter and the Sorcerer's Stone"),
            Booking(title="Fahrenheit 451"),
            Booking(title="A Wrinkle in Time")
        ]
        
        # Add each book to the database
        for book in book_list:
            book.create()
        print("Books added to the database.")
    else:
        print("Books already exist in the database.")
