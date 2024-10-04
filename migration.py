import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    conn = sqlite3.connect('construction_projects.db')
    cursor = conn.cursor()

    # Add foreign key constraints
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Add indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_name ON Projects (name);')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON Users (username);')

    # Add unique constraints
    cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_projects_name ON Projects (name);')
    cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS unique_users_username ON Users (username);')

    # Add data validation constraints
    cursor.execute('ALTER TABLE Budgets ADD CONSTRAINT chk_amount CHECK (amount >= 0);')
    cursor.execute('ALTER TABLE Tasks ADD CONSTRAINT chk_dates CHECK (start_date <= end_date);')

    conn.commit()
    conn.close()
    logger.info("Database migrations applied successfully")

if __name__ == "__main__":
    migrate_database()
