# model/literaryawardsdb.py
from __init__ import app, db
import logging

class LiteraryAward(db.Model):
    __tablename__ = 'literary_awards'
    
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), nullable=False)
    award_name = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=True)
    result = db.Column(db.String(50), nullable=True)  # e.g., "Winner", "Nominated"

    def __init__(self, book_title, award_name, year, category=None, result=None):
        self.book_title = book_title
        self.award_name = award_name
        self.year = year
        self.category = category
        self.result = result

    def create(self):
        """Create a new award entry in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error creating award entry: {str(e)}")
            return None
        return self
    
    def read(self):
        """Returns the award entry as a dictionary."""
        return {
            "id": self.id,
            "book_title": self.book_title,
            "award_name": self.award_name,
            "year": self.year,
            "category": self.category,
            "result": self.result
        }
    
    def update(self, data):
        """Updates the award entry with new data and commits the changes."""
        if not self:
            raise ValueError("Award entry does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error updating award entry: {str(e)}")
            raise e
    
    def delete(self):
        """Delete an award entry from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(f"Error deleting award entry: {str(e)}")
            raise e

    @staticmethod
    def restore(data):
        """Restores literary awards from the provided data."""
        for award_data in data:
            _ = award_data.pop('id', None)  # Remove 'id' from award_data
            award = LiteraryAward(**award_data)
            existing_award = LiteraryAward.query.filter_by(book_title=award.book_title, award_name=award.award_name, year=award.year).first()
            if existing_award:
                existing_award.update(award_data)
            else:
                award.create()
    
def initLiteraryAwards():
    # Check if any awards exist in the database
    if not LiteraryAward.query.first():
        # Create a list of sample award entries
        sample_awards = [
            LiteraryAward(book_title="The Road", award_name="Pulitzer Prize", year=2007, result="Winner"),
            LiteraryAward(book_title="The Goldfinch", award_name="Pulitzer Prize", year=2014, result="Winner"),
            LiteraryAward(book_title="A Visit from the Goon Squad", award_name="Pulitzer Prize", year=2011, result="Winner"),
        ]
        
        # Add each award to the database
        for award in sample_awards:
            award.create()
        print("Sample literary awards added to the database.")
    else:
        print("Literary awards already exist in the database.")
