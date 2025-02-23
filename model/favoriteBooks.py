from __init__ import app, db
import logging

class FavoriteBook(db.Model):
    __tablename__ = 'favorite_books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    
    def __init__(self, title):
        self.title = title

    def create(self):
        """Create a new favorite book entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating favorite book: {str(e)}")
            return None
        return self
    
    def read(self):
        """
        Returns the favorite book details as a dictionary.
        """
        return {
            "id": self.id,
            "title": self.title
        }
    
    def update(self, data):
        """
        Updates the favorite book with new data and commits the changes.
        """
        if not self:
            raise ValueError("Favorite book does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating favorite book: {str(e)}")
            raise e
    
    def delete(self):
        """Delete a favorite book entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting favorite book: {str(e)}")
            raise e
        
    @staticmethod
    def restore(data):
        """Restores favorite books from the provided data."""
        for favorite_book_data in data:
            _ = favorite_book_data.pop('id', None)  # Remove 'id' from favorite_book_data
            title = favorite_book_data.get("title", None)
            favorite_book = FavoriteBook.query.filter_by(title=title).first()
            if favorite_book:
                favorite_book.update(favorite_book_data)
            else:
                favorite_book = FavoriteBook(**favorite_book_data)
                favorite_book.create()
    
def initFavoriteBooks():
    # Check if any favorite books exist in the database
    if not FavoriteBook.query.first():
        # Create a list of favorite books to be added
        favorite_book_list = [
            FavoriteBook(title="Hunger Games"), 
            FavoriteBook(title="Maze Runner"),
        ]
        
        # Add each favorite book to the database
        for favorite_book in favorite_book_list:
            favorite_book.create()
        print("Favorite books added to the database.")
    else:
        print("Favorite books already exist in the database.")