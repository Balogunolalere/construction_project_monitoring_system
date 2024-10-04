import sqlite3
import logging
from contextlib import contextmanager
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('construction_projects.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def execute_query(query, params=(), fetchone=False):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        if fetchone:
            row = cursor.fetchone()
            return dict_from_row(row) if row else None
        return [dict_from_row(row) for row in cursor.fetchall()]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Project:
    @staticmethod
    def create(name, description, start_date, end_date):
        query = """INSERT INTO Projects (name, description, start_date, end_date)
                   VALUES (?, ?, ?, ?)"""
        execute_query(query, (name, description, start_date, end_date))
        logger.info(f"Project '{name}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Projects")

    @staticmethod
    def get_by_id(project_id):
        query = "SELECT * FROM Projects WHERE id = ?"
        result = execute_query(query, (project_id,), fetchone=True)
        if result is None:
            logger.warning(f"No project found with ID {project_id}")
        return result

    @staticmethod
    def update(project_id, name, description, start_date, end_date):
        query = """UPDATE Projects
                   SET name = ?, description = ?, start_date = ?, end_date = ?
                   WHERE id = ?"""
        execute_query(query, (name, description, start_date, end_date, project_id))
        updated_project = Project.get_by_id(project_id)
        if updated_project:
            logger.info(f"Project with ID {project_id} updated successfully")
            return updated_project
        logger.error(f"Update failed: Project with ID {project_id} not found after update")
        return None

    @staticmethod
    def delete(project_id):
        query = "DELETE FROM Projects WHERE id = ?"
        execute_query(query, (project_id,))
        logger.info(f"Project with ID {project_id} deleted successfully")

class File:
    @staticmethod
    def create(name, path):
        query = """INSERT INTO Files (name, path)
                   VALUES (?, ?)"""
        execute_query(query, (name, path))
        logger.info(f"File '{name}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Files")

    @staticmethod
    def get_by_id(file_id):
        query = "SELECT * FROM Files WHERE id = ?"
        result = execute_query(query, (file_id,), fetchone=True)
        if result is None:
            logger.warning(f"No file found with ID {file_id}")
        return result

    @staticmethod
    def update(file_id, name, path):
        query = """UPDATE Files
                   SET name = ?, path = ?
                   WHERE id = ?"""
        execute_query(query, (name, path, file_id))
        updated_file = File.get_by_id(file_id)
        if updated_file:
            logger.info(f"File with ID {file_id} updated successfully")
            return updated_file
        logger.error(f"Update failed: File with ID {file_id} not found after update")
        return None

    @staticmethod
    def delete(file_id):
        query = "DELETE FROM Files WHERE id = ?"
        execute_query(query, (file_id,))
        logger.info(f"File with ID {file_id} deleted successfully")

class Notification:
    @staticmethod
    def create(message, date):
        query = """INSERT INTO Notifications (message, date)
                   VALUES (?, ?)"""
        execute_query(query, (message, date))
        logger.info(f"Notification '{message}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Notifications")

    @staticmethod
    def get_by_id(notification_id):
        query = "SELECT * FROM Notifications WHERE id = ?"
        result = execute_query(query, (notification_id,), fetchone=True)
        if result is None:
            logger.warning(f"No notification found with ID {notification_id}")
        return result

    @staticmethod
    def update(notification_id, message, date):
        query = """UPDATE Notifications
                   SET message = ?, date = ?
                   WHERE id = ?"""
        execute_query(query, (message, date, notification_id))
        updated_notification = Notification.get_by_id(notification_id)
        if updated_notification:
            logger.info(f"Notification with ID {notification_id} updated successfully")
            return updated_notification
        logger.error(f"Update failed: Notification with ID {notification_id} not found after update")
        return None

    @staticmethod
    def delete(notification_id):
        query = "DELETE FROM Notifications WHERE id = ?"
        execute_query(query, (notification_id,))
        logger.info(f"Notification with ID {notification_id} deleted successfully")

class Resource:
    @staticmethod
    def create(name, type, availability):
        query = """INSERT INTO Resources (name, type, availability)
                   VALUES (?, ?, ?)"""
        execute_query(query, (name, type, availability))
        logger.info(f"Resource '{name}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Resources")

    @staticmethod
    def get_by_id(resource_id):
        query = "SELECT * FROM Resources WHERE id = ?"
        result = execute_query(query, (resource_id,), fetchone=True)
        if result is None:
            logger.warning(f"No resource found with ID {resource_id}")
        return result

    @staticmethod
    def update(resource_id, name, type, availability):
        query = """UPDATE Resources
                   SET name = ?, type = ?, availability = ?
                   WHERE id = ?"""
        execute_query(query, (name, type, availability, resource_id))
        updated_resource = Resource.get_by_id(resource_id)
        if updated_resource:
            logger.info(f"Resource with ID {resource_id} updated successfully")
            return updated_resource
        logger.error(f"Update failed: Resource with ID {resource_id} not found after update")
        return None

    @staticmethod
    def delete(resource_id):
        query = "DELETE FROM Resources WHERE id = ?"
        execute_query(query, (resource_id,))
        logger.info(f"Resource with ID {resource_id} deleted successfully")

class Task:
    @staticmethod
    def create(name, start_date, end_date, dependencies):
        query = """INSERT INTO Tasks (name, start_date, end_date, dependencies)
                   VALUES (?, ?, ?, ?)"""
        execute_query(query, (name, start_date, end_date, dependencies))
        logger.info(f"Task '{name}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Tasks")

    @staticmethod
    def get_by_id(task_id):
        query = "SELECT * FROM Tasks WHERE id = ?"
        result = execute_query(query, (task_id,), fetchone=True)
        if result is None:
            logger.warning(f"No task found with ID {task_id}")
        return result

    @staticmethod
    def update(task_id, name, start_date, end_date, dependencies):
        query = """UPDATE Tasks
                   SET name = ?, start_date = ?, end_date = ?, dependencies = ?
                   WHERE id = ?"""
        execute_query(query, (name, start_date, end_date, dependencies, task_id))
        updated_task = Task.get_by_id(task_id)
        if updated_task:
            logger.info(f"Task with ID {task_id} updated successfully")
            return updated_task
        logger.error(f"Update failed: Task with ID {task_id} not found after update")
        return None

    @staticmethod
    def delete(task_id):
        query = "DELETE FROM Tasks WHERE id = ?"
        execute_query(query, (task_id,))
        logger.info(f"Task with ID {task_id} deleted successfully")

class Budget:
    @staticmethod
    def create(project_id, amount, date):
        query = """INSERT INTO Budgets (project_id, amount, date)
                   VALUES (?, ?, ?)"""
        execute_query(query, (project_id, amount, date))
        logger.info(f"Budget for project ID '{project_id}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Budgets")

    @staticmethod
    def get_by_id(budget_id):
        query = "SELECT * FROM Budgets WHERE id = ?"
        result = execute_query(query, (budget_id,), fetchone=True)
        if result is None:
            logger.warning(f"No budget found with ID {budget_id}")
        return result

    @staticmethod
    def update(budget_id, project_id, amount, date):
        query = """UPDATE Budgets
                   SET project_id = ?, amount = ?, date = ?
                   WHERE id = ?"""
        execute_query(query, (project_id, amount, date, budget_id))
        updated_budget = Budget.get_by_id(budget_id)
        if updated_budget:
            logger.info(f"Budget with ID {budget_id} updated successfully")
            return updated_budget
        logger.error(f"Update failed: Budget with ID {budget_id} not found after update")
        return None

    @staticmethod
    def delete(budget_id):
        query = "DELETE FROM Budgets WHERE id = ?"
        execute_query(query, (budget_id,))
        logger.info(f"Budget with ID {budget_id} deleted successfully")

class Message:
    @staticmethod
    def create(from_user, to_user, content, date):
        query = """INSERT INTO Messages (from_user, to_user, content, date)
                   VALUES (?, ?, ?, ?)"""
        execute_query(query, (from_user, to_user, content, date))
        logger.info(f"Message from '{from_user}' to '{to_user}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Messages")

    @staticmethod
    def get_by_id(message_id):
        query = "SELECT * FROM Messages WHERE id = ?"
        result = execute_query(query, (message_id,), fetchone=True)
        if result is None:
            logger.warning(f"No message found with ID {message_id}")
        return result

    @staticmethod
    def update(message_id, from_user, to_user, content, date):
        query = """UPDATE Messages
                   SET from_user = ?, to_user = ?, content = ?, date = ?
                   WHERE id = ?"""
        execute_query(query, (from_user, to_user, content, date, message_id))
        updated_message = Message.get_by_id(message_id)
        if updated_message:
            logger.info(f"Message with ID {message_id} updated successfully")
            return updated_message
        logger.error(f"Update failed: Message with ID {message_id} not found after update")
        return None

    @staticmethod
    def delete(message_id):
        query = "DELETE FROM Messages WHERE id = ?"
        execute_query(query, (message_id,))
        logger.info(f"Message with ID {message_id} deleted successfully")

class Report:
    @staticmethod
    def create(name, content, date):
        query = """INSERT INTO Reports (name, content, date)
                   VALUES (?, ?, ?)"""
        execute_query(query, (name, content, date))
        logger.info(f"Report '{name}' created successfully")

    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM Reports")

    @staticmethod
    def get_by_id(report_id):
        query = "SELECT * FROM Reports WHERE id = ?"
        result = execute_query(query, (report_id,), fetchone=True)
        if result is None:
            logger.warning(f"No report found with ID {report_id}")
        return result

    @staticmethod
    def update(report_id, name, content, date):
        query = """UPDATE Reports
                   SET name = ?, content = ?, date = ?
                   WHERE id = ?"""
        execute_query(query, (name, content, date, report_id))
        updated_report = Report.get_by_id(report_id)
        if updated_report:
            logger.info(f"Report with ID {report_id} updated successfully")
            return updated_report
        logger.error(f"Update failed: Report with ID {report_id} not found after update")
        return None

    @staticmethod
    def delete(report_id):
        query = "DELETE FROM Reports WHERE id = ?"
        execute_query(query, (report_id,))
        logger.info(f"Report with ID {report_id} deleted successfully")

class User:
    @staticmethod
    def create(username, hashed_password, role='user'):
        query = """INSERT INTO Users (username, password, role)
               VALUES (?, ?, ?)"""
        execute_query(query, (username, hashed_password, role))
        logger.info(f"User '{username}' created successfully")

    @staticmethod
    def get_by_username(username):
        query = "SELECT * FROM Users WHERE username = ?"
        result = execute_query(query, (username,), fetchone=True)
        if result is None:
            logger.warning(f"No user found with username {username}")
        return result

    @staticmethod
    def update(username, password, role):
        hashed_password = hash_password(password)
        query = """UPDATE Users
                   SET password = ?, role = ?
                   WHERE username = ?"""
        execute_query(query, (hashed_password, role, username))
        updated_user = User.get_by_username(username)
        if updated_user:
            logger.info(f"User '{username}' updated successfully")
            return updated_user
        logger.error(f"Update failed: User '{username}' not found after update")
        return None

    @staticmethod
    def delete(username):
        query = "DELETE FROM Users WHERE username = ?"
        execute_query(query, (username,))
        logger.info(f"User '{username}' deleted successfully")

    @staticmethod
    def get_by_reset_token(token):
        query = "SELECT * FROM Users WHERE reset_token = ?"
        result = execute_query(query, (token,), fetchone=True)
        if result is None:
            logger.warning(f"No user found with reset token {token}")
        return result

    @staticmethod
    def update_password(username, new_password):
        hashed_password = hash_password(new_password)
        query = """UPDATE Users
                   SET password = ?
                   WHERE username = ?"""
        execute_query(query, (hashed_password, username))
        updated_user = User.get_by_username(username)
        if updated_user:
            logger.info(f"Password for user '{username}' updated successfully")
            return updated_user
        logger.error(f"Update failed: User '{username}' not found after update")
        return None
    
    @staticmethod
    def get_by_username(username):
        query = "SELECT * FROM Users WHERE username = ?"
        return execute_query(query, (username,), fetchone=True)

    @staticmethod
    def get_all():
        query = "SELECT * FROM Users"
        return execute_query(query)  # Fetch all users

# Initialize database
def initialize_database():
    with get_db_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS Projects
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         description TEXT,
                         start_date DATE,
                         end_date DATE)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Files
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         path TEXT NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Notifications
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         message TEXT NOT NULL,
                         date DATE NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Resources
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         type TEXT NOT NULL,
                         availability TEXT NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         start_date DATE NOT NULL,
                         end_date DATE NOT NULL,
                         dependencies TEXT)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Budgets
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         project_id INTEGER NOT NULL,
                         amount REAL NOT NULL,
                         date DATE NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Messages
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         from_user TEXT NOT NULL,
                         to_user TEXT NOT NULL,
                         content TEXT NOT NULL,
                         date DATE NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Reports
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         content TEXT NOT NULL,
                         date DATE NOT NULL)''')

        conn.execute('''CREATE TABLE IF NOT EXISTS Users
                        (username TEXT PRIMARY KEY,
                         password TEXT NOT NULL,
                         role TEXT NOT NULL,
                         reset_token TEXT)''')

        # Create default admin user
        admin_user = User.get_by_username("admin")
        if not admin_user:
            hashed_admin_password = hash_password("admin")
            User.create("admin", hashed_admin_password, "admin")

    logger.info("Database initialized successfully")

initialize_database()

