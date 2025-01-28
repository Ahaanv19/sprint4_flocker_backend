from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db
from sqlalchemy import inspect  # Ensure we import inspect for table name retrieval

class usersDb(db.Model):
    """
    =usersDb Model
    
    Represents a user with a name, fav_book, and a user_id.
    """
    __tablename__ = 'usersDb'

    table_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    fav_book = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Consider ForeignKey if this links to another table

    def __init__(self, name, fav_book, user_id):
        """
        Constructor for usersDb.
        """
        self.name = name
        self.fav_book = fav_book
        self.user_id = user_id

    def __repr__(self):
        """
        Represents the usersDb object as a string for debugging.
        """
        return f"<usersDb(id={self.table_id}, name='{self.name}', fav_book='{self.fav_book}', user_id={self.user_id})>"

    def create(self):
        """
        Adds the user to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error creating user: {str(e)}")

    def read(self):
        """
        Returns the user details as a dictionary.
        """
        return {
            "id": self.table_id,
            "name": self.name,
            "fav_book": self.fav_book,
            "user_id": self.user_id
        }

    def update(self, data):
        """
        Updates the quiz with new data and commits the changes.
        """
        if not self:
            raise ValueError("User does not exist.")
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error updating user: {str(e)}")

    def delete(self):
        """
        Deletes the quiz from the database and commits the transaction.
        """
        if not self:
            raise ValueError("User does not exist.")
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error deleting user: {str(e)}")


def initUserCreation():
    """
    Initializes the UserCreation table and inserts test data for development purposes.
    """
    with app.app_context():
        # Create the database and tables
        db.create_all()
        
        # Use the inspector to get table names
        inspector = inspect(db.engine)
        print(f"Tables created: {inspector.get_table_names()}")  # Debug message

        # Sample test data
        users = [
            usersDb(name="Arnav", fav_book="Maze Runner", user_id=1),
            usersDb(name="Ahaan", fav_book="Hunger Games", user_id=2),
            usersDb(name="John", fav_book="Example Book", user_id=3)
        ]

        for user in users:
            try:
                user.create()
                print(f"Created user: {user}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {user}")


