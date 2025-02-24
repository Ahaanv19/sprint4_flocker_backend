from __init__ import app, db
import logging

class BookProgress(db.Model):
    __tablename__ = 'book_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    percent_read = db.Column(db.Float, nullable=False, default=0.0)
    
    def __init__(self, title, percent_read=0.0):
        self.title = title
        self.percent_read = percent_read

    def create(self):
        """Create a new book progress entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating book progress: {str(e)}")
            return None
        return self
    
    def read(self):
        """
        Returns the book progress details as a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "percent_read": self.percent_read
        }
    
    def update(self, data):
        """
        Updates the book progress with new data and commits the changes.
        """
        if not self:
            raise ValueError("Book progress does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating book progress: {str(e)}")
            raise e
    
    def delete(self):
        """Delete a book progress entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting book progress: {str(e)}")
            raise e
        
    @staticmethod
    def restore(data):
        """Restores book progress from the provided data."""
        for book_progress_data in data:
            _ = book_progress_data.pop('id', None)  # Remove 'id' from book_progress_data
            title = book_progress_data.get("title", None)
            book_progress = BookProgress.query.filter_by(title=title).first()
            if book_progress:
                book_progress.update(book_progress_data)
            else:
                book_progress = BookProgress(**book_progress_data)
                book_progress.create()
    
def initBookProgress():
    # Check if any book progress entries exist in the database
    if not BookProgress.query.first():
        # Create a list of book progress entries to be added
        book_progress_list = [
            BookProgress(title="Hunger Games", percent_read=30.0), 
            BookProgress(title="Maze Runner", percent_read=50.0),
        ]
        
        # Add each book progress entry to the database
        for book_progress in book_progress_list:
            book_progress.create()
        print("Book progress entries added to the database.")
    else:
        print("Book progress entries already exist in the database.")
