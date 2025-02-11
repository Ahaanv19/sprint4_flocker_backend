from __init__ import app, db
import logging

class Quote(db.Model):
    __tablename__ = 'quotes'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    book = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=True)

    def __init__(self, text, book=None, author=None):
        self.text = text
        self.book = book
        self.author = author

    def create(self):
        """Create a new quote entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating quote: {str(e)}")
            return None
        return self
    
    def read(self):
        """Returns the quote details as a dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "book": self.book,
            "author": self.author
        }
    
    def update(self, data):
        """Updates the quote with new data and commits the changes."""
        if not self:
            raise ValueError("Quote does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating quote: {str(e)}")
            raise e
    
    def delete(self):
        """Delete a quote entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting quote: {str(e)}")
            raise e
        
    @staticmethod
    def restore(data):
        """Restores quotes from the provided data."""
        for quote_data in data:
            _ = quote_data.pop('id', None)  # Remove 'id' from quote_data
            text = quote_data.get("text", None)
            author = quote_data.get("author", None)
            quote = Quote.query.filter_by(text=text, author=author).first()
            if quote:
                quote.update(quote_data)
            else:
                quote = Quote(**quote_data)
                quote.create()

def initQuotes():
    # Check if any quotes exist in the database
    if not Quote.query.first():
        # Create a list of quotes to be added
        quote_list = [
            Quote(text="It is our choices, Harry, that show what we truly are, far more than our abilities.", book="Harry Potter and the Chamber of Secrets", author="J.K. Rowling"),
            Quote(text="The only way to do great work is to love what you do.", author="Steve Jobs"),
            Quote(text="Not all those who wander are lost.", book="The Lord of the Rings", author="J.R.R. Tolkien")
        ]
        
        # Add each quote to the database
        for quote in quote_list:
            quote.create()
        print("Quotes added to the database.")
    else:
        print("Quotes already exist in the database.")
