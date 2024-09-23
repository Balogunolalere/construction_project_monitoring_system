import streamlit as st
import bcrypt
from datetime import datetime
import os
import logging
from database import (
    create_project, read_projects, update_project, delete_project,
    create_task, read_tasks, read_tasks_by_project, update_task, delete_task,
    create_resource, read_resources, update_resource, delete_resource,
    create_file, read_files, read_files_by_project, update_file, delete_file,
    User, create_user, update_user, delete_user, get_notifications_by_user,
    create_notification
)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def login():
    """Handle user login."""
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = User.get_by_username(username)
            if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                st.success("Logged in successfully!")
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user['role']
                st.session_state["user_id"] = user['id']
                logging.info(f"User {username} logged in successfully")
            else:
                st.error("Invalid username or password")
                logging.warning(f"Failed login attempt for username: {username}")
        except Exception as e:
            st.error("An error occurred during login. Please try again.")
            logging.error(f"Login error: {str(e)}")

def register():
    """Handle user registration."""
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            try:
                user = User.get_by_username(username)
                if user:
                    st.error("Username already taken")
                else:
                    create_user(username, password, "user")
                    st.success("Account created successfully!")
                    logging.info(f"User {username} registered successfully")
            except Exception as e:
                st.error("An error occurred during registration. Please try again.")
                logging.error(f"Registration error: {str(e)}")


def main():
    """Main application logic."""
    st.title("Construction Project Monitoring System")

    menu = ["Projects", "Tasks", "Resources", "Files", "Users", "Notifications"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Projects":
        st.subheader("Projects")
        if st.session_state["role"] == "admin":
            manage_projects()
        view_projects()

    elif choice == "Tasks":
        st.subheader("Tasks")
        if st.session_state["role"] == "admin":
            manage_tasks()
        view_tasks()

    elif choice == "Resources":
        st.subheader("Resources")
        if st.session_state["role"] == "admin":
            manage_resources()
        view_resources()

    elif choice == "Files":
        st.subheader("Files")
        if st.session_state["role"] == "admin":
            manage_files()
        view_files()

    elif choice == "Users":
        st.subheader("Users")
        if st.session_state["role"] == "admin":
            manage_users()
        else:
            st.warning("You do not have permission to manage users.")

    elif choice == "Notifications":
        st.subheader("Notifications")
        view_notifications()

    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.session_state["user_id"] = None
        logging.info(f"User {st.session_state.get('username')} logged out")
        st.rerun()

    st.sidebar.write("Logged in as:", st.session_state["username"])
    st.sidebar.write("Role:", st.session_state["role"])

def manage_projects():
    """Handle project management operations."""
    st.subheader("Manage Projects")

    with st.form("Create Project"):
        project_name = st.text_input("Project Name")
        project_description = st.text_area("Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        submitted = st.form_submit_button("Create Project")
        if submitted:
            try:
                create_project(project_name, project_description, start_date, end_date)
                st.success(f"Project '{project_name}' created successfully!")
                logging.info(f"Project '{project_name}' created by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], None, f"New project '{project_name}' created")
            except Exception as e:
                st.error(f"An error occurred while creating the project: {str(e)}")
                logging.error(f"Error creating project: {str(e)}")

    projects = read_projects()
    for project in projects:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"ID: {project['id']}, Name: {project['name']}, Description: {project['description']}")
        with col2:
            if st.button(f"Update Project {project['name']}", key=f"update_{project['id']}"):
                update_project_form(project)
        with col3:
            if st.button(f"Delete Project {project['name']}", key=f"delete_{project['id']}"):
                try:
                    delete_project(project['id'])
                    st.success(f"Project '{project['name']}' deleted successfully!")
                    logging.info(f"Project '{project['name']}' deleted by {st.session_state['username']}")
                    create_notification(st.session_state["user_id"], None, f"Project '{project['name']}' deleted")
                except Exception as e:
                    st.error(f"An error occurred while deleting the project: {str(e)}")
                    logging.error(f"Error deleting project: {str(e)}")

def update_project_form(project):
    """Display form for updating a project."""
    with st.form(f"Update Project {project['name']}"):
        project_name = st.text_input("Project Name", value=project['name'])
        project_description = st.text_area("Description", value=project['description'])
        start_date = st.date_input("Start Date", value=datetime.strptime(project['start_date'], "%Y-%m-%d").date())
        end_date = st.date_input("End Date", value=datetime.strptime(project['end_date'], "%Y-%m-%d").date())
        submitted = st.form_submit_button("Update Project")
        if submitted:
            try:
                update_project(project['id'], project_name, project_description, start_date, end_date)
                st.success(f"Project '{project_name}' updated successfully!")
                logging.info(f"Project '{project_name}' updated by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], project['id'], f"Project '{project_name}' updated")
            except Exception as e:
                st.error(f"An error occurred while updating the project: {str(e)}")
                logging.error(f"Error updating project: {str(e)}")

def view_projects():
    """Display all projects."""
    st.subheader("View Projects")
    projects = read_projects()
    for project in projects:
        st.write(f"ID: {project['id']}, Name: {project['name']}, Description: {project['description']}")
        st.write(f"Start Date: {project['start_date']}, End Date: {project['end_date']}")
        st.write("---")

        display_project_tasks(project['id'])
        display_project_resources(project['id'])
        display_project_files(project['id'])

def display_project_tasks(project_id):
    """Display tasks associated with a project."""
    tasks = read_tasks_by_project(project_id)
    if tasks:
        st.write("Tasks:")
        for task in tasks:
            st.write(f"- {task['name']} (Status: {task['status']})")
    else:
        st.write("No tasks found for this project.")

def display_project_resources(project_id):
    """Display resources associated with a project."""
    resources = read_resources()  # Assuming there is no direct relation between projects and resources
    if resources:
        st.write("Resources:")
        for resource in resources:
            st.write(f"- {resource['name']} ({resource['type']})")
    else:
        st.write("No resources found.")

def display_project_files(project_id):
    """Display files associated with a project."""
    files = read_files_by_project(project_id)
    if files:
        st.write("Files:")
        for file in files:
            st.write(f"- {file['name']} (Version: {file['version']})")
    else:
        st.write("No files found for this project.")

def manage_tasks():
    """Handle task management operations."""
    st.subheader("Manage Tasks")

    with st.form("Create Task"):
        project_id = st.selectbox("Project", [project['id'] for project in read_projects()], format_func=lambda x: str(x))
        task_name = st.text_input("Task Name")
        task_description = st.text_area("Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        submitted = st.form_submit_button("Create Task")
        if submitted:
            try:
                create_task(project_id, task_name, task_description, start_date, end_date, status)
                st.success(f"Task '{task_name}' created successfully!")
                logging.info(f"Task '{task_name}' created by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], project_id, f"New task '{task_name}' created")
            except Exception as e:
                st.error(f"An error occurred while creating the task: {str(e)}")
                logging.error(f"Error creating task: {str(e)}")

    tasks = read_tasks()
    for task in tasks:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"ID: {task['id']}, Name: {task['name']}, Project: {task['project_id']}, Status: {task['status']}")
        with col2:
            if st.button(f"Update Task {task['name']}", key=f"update_task_{task['id']}"):
                update_task_form(task)
        with col3:
            if st.button(f"Delete Task {task['name']}", key=f"delete_task_{task['id']}"):
                try:
                    delete_task(task['id'])
                    st.success(f"Task '{task['name']}' deleted successfully!")
                    logging.info(f"Task '{task['name']}' deleted by {st.session_state['username']}")
                    create_notification(st.session_state["user_id"], task['project_id'], f"Task '{task['name']}' deleted")
                except Exception as e:
                    st.error(f"An error occurred while deleting the task: {str(e)}")
                    logging.error(f"Error deleting task: {str(e)}")

def update_task_form(task):
    """Display form for updating a task."""
    with st.form(f"Update Task {task['name']}"):
        task_name = st.text_input("Task Name", value=task['name'])
        task_description = st.text_area("Description", value=task['description'])
        start_date = st.date_input("Start Date", value=task['start_date'])
        end_date = st.date_input("End Date", value=task['end_date'])
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(task['status']))
        submitted = st.form_submit_button("Update Task")
        if submitted:
            try:
                update_task(task['id'], task_name, task_description, start_date, end_date, status)
                st.success(f"Task '{task_name}' updated successfully!")
                logging.info(f"Task '{task_name}' updated by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], task['project_id'], f"Task '{task_name}' updated")
            except Exception as e:
                st.error(f"An error occurred while updating the task: {str(e)}")
                logging.error(f"Error updating task: {str(e)}")

def view_tasks():
    """Display all tasks."""
    st.subheader("View Tasks")
    tasks = read_tasks()
    for task in tasks:
        st.write(f"ID: {task['id']}, Name: {task['name']}, Project: {task['project_id']}, Status: {task['status']}")
        st.write(f"Start Date: {task['start_date']}, End Date: {task['end_date']}")
        st.write(f"Description: {task['description']}")
        st.write("---")

def manage_resources():
    """Handle resource management operations."""
    st.subheader("Manage Resources")

    with st.form("Create Resource"):
        resource_name = st.text_input("Resource Name")
        resource_type = st.text_input("Resource Type")
        available_from = st.date_input("Available From")
        available_to = st.date_input("Available To")
        submitted = st.form_submit_button("Create Resource")
        if submitted:
            try:
                create_resource(resource_name, resource_type, available_from, available_to)
                st.success(f"Resource '{resource_name}' created successfully!")
                logging.info(f"Resource '{resource_name}' created by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], None, f"New resource '{resource_name}' created")
            except Exception as e:
                st.error(f"An error occurred while creating the resource: {str(e)}")
                logging.error(f"Error creating resource: {str(e)}")

    resources = read_resources()
    for resource in resources:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"ID: {resource['id']}, Name: {resource['name']}, Type: {resource['type']}")
        with col2:
            if st.button(f"Update Resource {resource['name']}", key=f"update_resource_{resource['id']}"):
                update_resource_form(resource)
        with col3:
            if st.button(f"Delete Resource {resource['name']}", key=f"delete_resource_{resource['id']}"):
                try:
                    delete_resource(resource['id'])
                    st.success(f"Resource '{resource['name']}' deleted successfully!")
                    logging.info(f"Resource '{resource['name']}' deleted by {st.session_state['username']}")
                    create_notification(st.session_state["user_id"], None, f"Resource '{resource['name']}' deleted")
                except Exception as e:
                    st.error(f"An error occurred while deleting the resource: {str(e)}")
                    logging.error(f"Error deleting resource: {str(e)}")

def update_resource_form(resource):
    """Display form for updating a resource."""
    with st.form(f"Update Resource {resource['name']}"):
        resource_name = st.text_input("Resource Name", value=resource['name'])
        resource_type = st.text_input("Resource Type", value=resource['type'])
        available_from = st.date_input("Available From", value=resource['available_from'])
        available_to = st.date_input("Available To", value=resource['available_to'])
        submitted = st.form_submit_button("Update Resource")
        if submitted:
            try:
                update_resource(resource['id'], resource_name, resource_type, available_from, available_to)
                st.success(f"Resource '{resource_name}' updated successfully!")
                logging.info(f"Resource '{resource_name}' updated by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], None, f"Resource '{resource_name}' updated")
            except Exception as e:
                st.error(f"An error occurred while updating the resource: {str(e)}")
                logging.error(f"Error updating resource: {str(e)}")

def view_resources():
    """Display all resources."""
    st.subheader("View Resources")
    resources = read_resources()
    for resource in resources:
        st.write(f"ID: {resource['id']}, Name: {resource['name']}, Type: {resource['type']}")
        st.write(f"Available From: {resource['available_from']}, Available To: {resource['available_to']}")
        st.write("---")

def manage_files():
    """Handle file management operations."""
    st.subheader("Manage Files")

    with st.form("Upload File"):
        project_id = st.selectbox("Project", [project['id'] for project in read_projects()], format_func=lambda x: str(x))
        file = st.file_uploader("Choose a file")
        submitted = st.form_submit_button("Upload File")
        if submitted and file is not None:
            try:
                file_name = file.name
                uploads_dir = "uploads"
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, file_name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                version = 1
                uploaded_by = st.session_state["username"]
                create_file(project_id, file_name, file_path, version, uploaded_by)
                st.success(f"File '{file_name}' uploaded successfully!")
                logging.info(f"File '{file_name}' uploaded by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], project_id, f"New file '{file_name}' uploaded")
            except Exception as e:
                st.error(f"An error occurred while uploading the file: {str(e)}")
                logging.error(f"Error uploading file: {str(e)}")

    files = read_files()
    for file in files:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"ID: {file['id']}, Name: {file['name']}, Project: {file['project_id']}, Version: {file['version']}, Uploaded By: {file['uploaded_by']}, Uploaded At: {file['uploaded_at']}")
        with col2:
            if st.button(f"Update File {file['name']}", key=f"update_file_{file['id']}"):
                update_file_form(file)
        with col3:
            if st.button(f"Delete File {file['name']}", key=f"delete_file_{file['id']}"):
                try:
                    delete_file(file['id'])
                    st.success(f"File '{file['name']}' deleted successfully!")
                    logging.info(f"File '{file['name']}' deleted by {st.session_state['username']}")
                    create_notification(st.session_state["user_id"], file['project_id'], f"File '{file['name']}' deleted")
                except Exception as e:
                    st.error(f"An error occurred while deleting the file: {str(e)}")
                    logging.error(f"Error deleting file: {str(e)}")

def update_file_form(file):
    """Display form for updating a file."""
    with st.form(f"Update File {file['name']}"):
        file_name = st.text_input("File Name", value=file['name'])
        new_file = st.file_uploader("Choose a new file", key=f"update_{file['id']}")
        submitted = st.form_submit_button("Update File")
        if submitted:
            try:
                if new_file is not None:
                    file_path = os.path.join("uploads", new_file.name)
                    with open(file_path, "wb") as f:
                        f.write(new_file.getbuffer())
                else:
                    file_path = file['file_path']
                new_version = update_file(file['id'], file_name, file_path)
                st.success(f"File '{file_name}' updated successfully! New version: {new_version}")
                logging.info(f"File '{file_name}' updated by {st.session_state['username']}")
                create_notification(st.session_state["user_id"], file['project_id'], f"File '{file_name}' updated to version {new_version}")
            except Exception as e:
                st.error(f"An error occurred while updating the file: {str(e)}")
                logging.error(f"Error updating file: {str(e)}")

def view_files():
    """Display all files."""
    st.subheader("View Files")
    files = read_files()
    for file in files:
        if is_user_associated_with_project(st.session_state["username"], file['project_id']):
            st.write(f"ID: {file['id']}, Name: {file['name']}, Project: {file['project_id']}, Version: {file['version']}, Uploaded By: {file['uploaded_by']}, Uploaded At: {file['uploaded_at']}")
            st.write("---")
        else:
            st.warning(f"You do not have permission to view files for the project with ID {file['project_id']}.")

def is_user_associated_with_project(username, project_id):
    """Check if a user is associated with a project."""
    # TODO: Implement proper authorization logic
    return True

def manage_users():
    """Handle user management operations."""
    st.subheader("Manage Users")

    with st.form("Create User"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "user"])
        submitted = st.form_submit_button("Create User")
        if submitted:
            try:
                create_user(username, password, role)
                st.success(f"User '{username}' created successfully!")
                logging.info(f"User '{username}' created by {st.session_state['username']}")
            except Exception as e:
                st.error(f"An error occurred while creating the user: {str(e)}")
                logging.error(f"Error creating user: {str(e)}")

    users = User.get_all()
    for user in users:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"ID: {user['id']}, Username: {user['username']}, Role: {user['role']}")
        with col2:
            if st.button(f"Update User {user['username']}", key=f"update_user_{user['id']}"):
                update_user_form(user)
        with col3:
            if st.button(f"Delete User {user['username']}", key=f"delete_user_{user['id']}"):
                try:
                    delete_user(user['id'])
                    st.success(f"User '{user['username']}' deleted successfully!")
                    logging.info(f"User '{user['username']}' deleted by {st.session_state['username']}")
                except Exception as e:
                    st.error(f"An error occurred while deleting the user: {str(e)}")
                    logging.error(f"Error deleting user: {str(e)}")

def update_user_form(user):
    """Display form for updating a user."""
    with st.form(f"Update User {user['username']}"):
        username = st.text_input("Username", value=user['username'])
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "user"], index=["admin", "user"].index(user['role']))
        submitted = st.form_submit_button("Update User")
        if submitted:
            try:
                update_user(user['id'], username, password, role)
                st.success(f"User '{username}' updated successfully!")
                logging.info(f"User '{username}' updated by {st.session_state['username']}")
            except Exception as e:
                st.error(f"An error occurred while updating the user: {str(e)}")
                logging.error(f"Error updating user: {str(e)}")

def view_notifications():
    """Display user-specific notifications."""
    user_notifications = get_notifications_by_user(st.session_state["user_id"])
    if user_notifications:
        for notification in user_notifications:
            st.write(f"Project: {notification['project_id']}, Message: {notification['message']}, Sent At: {notification['sent_at']}")
    else:
        st.write("No notifications found.")

if __name__ == "__main__":
    if not st.session_state.get("authenticated", False):
        choice = st.sidebar.selectbox("Menu", ["Login", "Register"])
        if choice == "Login":
            login()
        elif choice == "Register":
            register()
    else:
        main()