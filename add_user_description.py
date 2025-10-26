"""
Migration script to add user_description column to User table
Run this once to update your existing database.
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(user)"))
            columns = [row[1] for row in result]
            
            if 'user_description' not in columns:
                print("Adding user_description column to User table...")
                db.session.execute(text("ALTER TABLE user ADD COLUMN user_description TEXT"))
                db.session.commit()
                print("✓ Successfully added user_description column!")
            else:
                print("✓ user_description column already exists!")
                
        except Exception as e:
            print(f"✗ Error during migration: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()

