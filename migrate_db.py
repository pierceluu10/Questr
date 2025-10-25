#!/usr/bin/env python3
"""
Database migration script to add the DailyQuest table.
Run this script to update your database schema.
"""

from app import app, db
from models import DailyQuest

def migrate():
    with app.app_context():
        # Create all tables (this will create DailyQuest if it doesn't exist)
        db.create_all()
        print("✅ Database migration complete! DailyQuest table has been created.")
        print("You can now use the quest reroll feature.")

if __name__ == '__main__':
    migrate()

