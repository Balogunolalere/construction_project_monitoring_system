import sqlite3
import threading
import bcrypt
from datetime import datetime
import os

# Thread-local storage
thread_local = threading.local()

def get_conn():
    if not hasattr(thread_local, "conn"):
        thread_local.conn = sqlite3.connect('construction_projects.db')
        thread_local.conn.row_factory = sqlite3.Row
    return thread_local.conn

def get_cursor():
    if not hasattr(thread_local, "cursor"):
        thread_local.cursor = get_conn().cursor()
    return thread_local.cursor

# Create the tables
conn = get_conn()
cursor = get_cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Projects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  start_date DATE,
                  end_date DATE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  project_id INTEGER,
                  name TEXT NOT NULL,
                  description TEXT,
                  start_date DATE,
                  end_date DATE,
                  status TEXT,
                  FOREIGN KEY(project_id) REFERENCES Projects(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Resources
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT,
                  available_from DATE,
                  available_to DATE)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  project_id INTEGER,
                  name TEXT NOT NULL,
                  file_path TEXT NOT NULL,
                  version INTEGER,
                  uploaded_by TEXT,
                  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(project_id) REFERENCES Projects(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Notifications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  project_id INTEGER,
                  message TEXT NOT NULL,
                  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES Users(id),
                  FOREIGN KEY(project_id) REFERENCES Projects(id))''')

conn.commit()

class Project:
    def __init__(self, name, description, start_date, end_date):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Projects (name, description, start_date, end_date) VALUES (?, ?, ?, ?)",
                       (self.name, self.description, self.start_date, self.end_date))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Projects")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(project_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Projects WHERE id=?", (project_id,))
        return cursor.fetchone()

    @staticmethod
    def update(project_id, name, description, start_date, end_date):
        cursor = get_cursor()
        cursor.execute("UPDATE Projects SET name=?, description=?, start_date=?, end_date=? WHERE id=?",
                       (name, description, start_date, end_date, project_id))
        get_conn().commit()

    @staticmethod
    def delete(project_id):
        cursor = get_cursor()
        cursor.execute("DELETE FROM Projects WHERE id=?", (project_id,))
        get_conn().commit()

class Task:
    def __init__(self, project_id, name, description, start_date, end_date, status):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Tasks (project_id, name, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.project_id, self.name, self.description, self.start_date, self.end_date, self.status))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Tasks")
        return cursor.fetchall()

    @staticmethod
    def get_by_project(project_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Tasks WHERE project_id=?", (project_id,))
        return cursor.fetchall()

    @staticmethod
    def update(task_id, name, description, start_date, end_date, status):
        cursor = get_cursor()
        cursor.execute("UPDATE Tasks SET name=?, description=?, start_date=?, end_date=?, status=? WHERE id=?",
                       (name, description, start_date, end_date, status, task_id))
        get_conn().commit()

    @staticmethod
    def delete(task_id):
        cursor = get_cursor()
        cursor.execute("DELETE FROM Tasks WHERE id=?", (task_id,))
        get_conn().commit()

class Resource:
    def __init__(self, name, type, available_from, available_to):
        self.name = name
        self.type = type
        self.available_from = available_from
        self.available_to = available_to

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Resources (name, type, available_from, available_to) VALUES (?, ?, ?, ?)",
                       (self.name, self.type, self.available_from, self.available_to))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Resources")
        return cursor.fetchall()

    @staticmethod
    def update(resource_id, name, type, available_from, available_to):
        cursor = get_cursor()
        cursor.execute("UPDATE Resources SET name=?, type=?, available_from=?, available_to=? WHERE id=?",
                       (name, type, available_from, available_to, resource_id))
        get_conn().commit()

    @staticmethod
    def delete(resource_id):
        cursor = get_cursor()
        cursor.execute("DELETE FROM Resources WHERE id=?", (resource_id,))
        get_conn().commit()

class File:
    def __init__(self, project_id, name, file_path, version, uploaded_by):
        self.project_id = project_id
        self.name = name
        self.file_path = file_path
        self.version = version
        self.uploaded_by = uploaded_by

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Files (project_id, name, file_path, version, uploaded_by) VALUES (?, ?, ?, ?, ?)",
                       (self.project_id, self.name, self.file_path, self.version, self.uploaded_by))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_all():
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Files")
        return cursor.fetchall()

    @staticmethod
    def get_by_project(project_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Files WHERE project_id=?", (project_id,))
        return cursor.fetchall()

    @staticmethod
    def update(file_id, name, file_path):
        cursor = get_cursor()
        cursor.execute("UPDATE Files SET name=?, file_path=?, version=version+1 WHERE id=?",
                       (name, file_path, file_id))
        get_conn().commit()
        cursor.execute("SELECT version FROM Files WHERE id=?", (file_id,))
        return cursor.fetchone()['version']

    @staticmethod
    def delete(file_id):
        cursor = get_cursor()
        cursor.execute("DELETE FROM Files WHERE id=?", (file_id,))
        get_conn().commit()

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = self._hash_password(password)
        self.role = role

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                       (self.username, self.password, self.role))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_username(username):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        return cursor.fetchone()

    @staticmethod
    def get_all():
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()

    @staticmethod
    def update(user_id, username, password, role):
        cursor = get_cursor()
        hashed_password = User._hash_password(password)
        cursor.execute("UPDATE Users SET username=?, password=?, role=? WHERE id=?",
                       (username, hashed_password, role, user_id))
        get_conn().commit()

    @staticmethod
    def delete(user_id):
        cursor = get_cursor()
        cursor.execute("DELETE FROM Users WHERE id=?", (user_id,))
        get_conn().commit()

class Notification:
    def __init__(self, user_id, project_id, message):
        self.user_id = user_id
        self.project_id = project_id
        self.message = message

    def save(self):
        cursor = get_cursor()
        cursor.execute("INSERT INTO Notifications (user_id, project_id, message) VALUES (?, ?, ?)",
                       (self.user_id, self.project_id, self.message))
        get_conn().commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_user(user_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Notifications WHERE user_id=? ORDER BY sent_at DESC", (user_id,))
        return cursor.fetchall()

    @staticmethod
    def get_by_project(project_id):
        cursor = get_cursor()
        cursor.execute("SELECT * FROM Notifications WHERE project_id=? ORDER BY sent_at DESC", (project_id,))
        return cursor.fetchall()

def create_notification(user_id, project_id, message):
    notification = Notification(user_id, project_id, message)
    return notification.save()

def get_notifications_by_user(user_id):
    return Notification.get_by_user(user_id)

def get_notifications_by_project(project_id):
    return Notification.get_by_project(project_id)

def create_project(name, description, start_date, end_date):
    project = Project(name, description, start_date, end_date)
    return project.save()

def read_projects():
    return Project.get_all()

def update_project(project_id, name, description, start_date, end_date):
    return Project.update(project_id, name, description, start_date, end_date)

def delete_project(project_id):
    return Project.delete(project_id)

def create_task(project_id, name, description, start_date, end_date, status):
    task = Task(project_id, name, description, start_date, end_date, status)
    return task.save()

def read_tasks():
    return Task.get_all()

def read_tasks_by_project(project_id):
    return Task.get_by_project(project_id)

def update_task(task_id, name, description, start_date, end_date, status):
    return Task.update(task_id, name, description, start_date, end_date, status)

def delete_task(task_id):
    return Task.delete(task_id)

def create_resource(name, type, available_from, available_to):
    resource = Resource(name, type, available_from, available_to)
    return resource.save()

def read_resources():
    return Resource.get_all()

def update_resource(resource_id, name, type, available_from, available_to):
    return Resource.update(resource_id, name, type, available_from, available_to)

def delete_resource(resource_id):
    return Resource.delete(resource_id)

def create_file(project_id, name, file_path, version, uploaded_by):
    file = File(project_id, name, file_path, version, uploaded_by)
    return file.save()

def read_files():
    return File.get_all()

def read_files_by_project(project_id):
    return File.get_by_project(project_id)

def update_file(file_id, name, file_path):
    return File.update(file_id, name, file_path)

def delete_file(file_id):
    return File.delete(file_id)

def create_user(username, password, role):
    user = User(username, password, role)
    return user.save()

def update_user(user_id, username, password, role):
    return User.update(user_id, username, password, role)

def delete_user(user_id):
    return User.delete(user_id)

def initialize_database():
    cursor = get_cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    count = cursor.fetchone()[0]

    if count == 0:
        # Create an initial admin user
        admin_username = "admin"
        admin_password = "admin"
        admin_role = "admin"
        create_user(admin_username, admin_password, admin_role)
        print(f"Initial admin user created: Username = {admin_username}, Password = {admin_password}")

initialize_database()
