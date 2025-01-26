from __init__ import app, db
import logging

class Booking(db.Model):
    __tablename__ = 'booking'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    author = db.Column(db.String(255), nullable=False) 
    genre = db.Column(db.String(255), nullable=False)   
    
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

    def create(self):
        """Create a new booking entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating booking: {str(e)}")
            return None
        return self
    
    def read(self):
        """Returns the booking details as a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author, 
            "genre": self.genre     
        }
    
    def update(self, data):
        """Updates the booking with new data and commits the changes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating booking: {str(e)}")
            raise e
    
    def delete(self):
        """Delete a booking entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting booking: {str(e)}")
            raise e
        
    @staticmethod
    def restore(data):
        """Restores bookings from the provided data."""
        for booking_data in data:  
            _ = booking_data.pop('id', None) 

            title = booking_data.get("title", None)
            author = booking_data.get("author", None)
            genre = booking_data.get("genre", None)
            
            if title is None or author is None or genre is None:
                print(f"Missing required data for booking: {booking_data}")
                continue

            booking = Booking.query.filter_by(title=title).first()
            if booking:
                booking.update(booking_data)
            else:
                booking = Booking(title=title, author=author, genre=genre)
                booking.create()

def initbooking():  # Renamed from initbooking to initBookingEntries
    """Initializes the booking table with sample data if empty."""
    with app.app_context():
        if not Booking.query.first():
            book_list = [
                Booking(title="Noah's Great Demise", author="Author A", genre="Fiction"), 
                Booking(title="18 Days of School", author="Author B", genre="Non-Fiction"),
                Booking(title="To Kill a Mockingbird", author="Harper Lee", genre="Fiction"),
                Booking(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", genre="Fantasy"),
                Booking(title="Fahrenheit 451", author="Ray Bradbury", genre="Dystopian"),
                Booking(title="A Wrinkle in Time", author="Madeleine L'Engle", genre="Science Fiction")
            ]
            
            for booking in book_list:
                booking.create()
            print("Bookings added to the database.")
        else:
            print("Bookings already exist in the database.")
