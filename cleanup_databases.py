from main import app, db
from sqlalchemy import text  # Import 'text' from SQLAlchemy to handle raw SQL

def remove_tables():
    with app.app_context():  # Ensure you have an app context for interacting with the database
        tables = ['newbook', 'weathers']  # List of tables to remove

        for table in tables:
            try:
                # Use 'text()' to explicitly declare the SQL expression
                db.session.execute(text(f'DROP TABLE IF EXISTS {table}'))
                db.session.commit()  # Commit the transaction
                print(f'Successfully removed table: {table}')
            except Exception as e:
                db.session.rollback()  # Rollback in case of an error
                print(f"Error removing table {table}: {str(e)}")

if __name__ == '__main__':
    remove_tables()
