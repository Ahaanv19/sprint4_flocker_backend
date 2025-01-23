from main import app, db
from sqlalchemy import text  

def remove_tables():
    with app.app_context():  
        tables = ['table names here']  # List of tables to remove, run db_init.py to recreate them

        for table in tables:
            try:
                
                db.session.execute(text(f'DROP TABLE IF EXISTS {table}'))
                db.session.commit()  
                print(f'Successfully removed table: {table}')
            except Exception as e:
                db.session.rollback()  
                print(f"Error removing table {table}: {str(e)}")

if __name__ == '__main__':
    remove_tables()

