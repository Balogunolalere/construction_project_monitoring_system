import streamlit as st
from datetime import datetime
import logging
from database import Project, File, Notification, Resource, Task, Budget, Message, Report, User
from auth import login, register, check_login, logout

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Construction Project Management System")

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login_register()
    else:
        menu = ["View Projects", "Manage Projects", "File Management", "Notifications", "Resource Management", "Project Planning", "Budget Management", "Communication", "Reporting", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "View Projects":
            view_projects()
        elif choice == "Manage Projects":
            manage_projects()
        elif choice == "File Management":
            file_management()
        elif choice == "Notifications":
            notifications()
        elif choice == "Resource Management":
            resource_management()
        elif choice == "Project Planning":
            project_planning()
        elif choice == "Budget Management":
            budget_management()
        elif choice == "Communication":
            communication()
        elif choice == "Reporting":
            reporting()
        elif choice == "Logout":
            logout(st.session_state)
            st.rerun()

def login_register():
    st.subheader("Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register(new_username, new_password):
                st.success("Registered successfully! Please login.")
            else:
                st.error("Registration failed. Username may already exist.")

def view_projects():
    st.subheader("View Projects")
    projects = Project.get_all()
    for project in projects:
        st.write(f"ID: {project['id']}, Name: {project['name']}")
        st.write(f"Description: {project['description']}")
        st.write(f"Start Date: {project['start_date']}, End Date: {project['end_date']}")
        st.write("---")

def manage_projects():
    st.subheader("Manage Projects")

    # Create new project
    with st.form("Create Project"):
        st.write("Create New Project")
        project_name = st.text_input("Project Name")
        project_description = st.text_area("Description")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        if st.form_submit_button("Create Project"):
            try:
                Project.create(project_name, project_description, start_date, end_date)
                st.success(f"Project '{project_name}' created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating project: {str(e)}")

    # List and update projects
    projects = Project.get_all()
    for project in projects:
        with st.expander(f"Project: {project['name']}"):
            with st.form(f"Update Project {project['id']}"):
                updated_name = st.text_input("Name", value=project['name'])
                updated_description = st.text_area("Description", value=project['description'])
                updated_start_date = st.date_input("Start Date", value=datetime.strptime(project['start_date'], "%Y-%m-%d").date())
                updated_end_date = st.date_input("End Date", value=datetime.strptime(project['end_date'], "%Y-%m-%d").date())

                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Update"):
                        try:
                            updated_project = Project.update(project['id'], updated_name, updated_description, updated_start_date, updated_end_date)
                            if updated_project:
                                st.success(f"Project '{updated_name}' updated successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to update project.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            logger.error(f"Error updating project: {str(e)}")

                with col2:
                    if st.form_submit_button("Delete"):
                        try:
                            Project.delete(project['id'])
                            st.success(f"Project '{project['name']}' deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            logger.error(f"Error deleting project: {str(e)}")

def file_management():
    st.subheader("File Management")
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "cad", "jpg", "png"])
    if uploaded_file is not None:
        file_path = f"uploads/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        File.create(uploaded_file.name, file_path)

    files = File.get_all()
    for file in files:
        st.write(f"ID: {file['id']}, Name: {file['name']}, Path: {file['path']}")
        st.write("---")

def notifications():
    st.subheader("Notifications")
    notifications = Notification.get_all()
    for notification in notifications:
        st.write(f"Message: {notification['message']}")
        st.write(f"Date: {notification['date']}")
        st.write("---")

    with st.form("Create Notification"):
        message = st.text_area("Message")
        date = st.date_input("Date")
        if st.form_submit_button("Create Notification"):
            try:
                Notification.create(message, date)
                st.success("Notification created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating notification: {str(e)}")

def resource_management():
    st.subheader("Resource Management")
    resources = Resource.get_all()
    for resource in resources:
        st.write(f"ID: {resource['id']}, Name: {resource['name']}, Type: {resource['type']}")
        st.write(f"Availability: {resource['availability']}")
        st.write("---")

    with st.form("Create Resource"):
        name = st.text_input("Name")
        type = st.text_input("Type")
        availability = st.text_input("Availability")
        if st.form_submit_button("Create Resource"):
            try:
                Resource.create(name, type, availability)
                st.success("Resource created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating resource: {str(e)}")

def project_planning():
    st.subheader("Project Planning")
    tasks = Task.get_all()
    for task in tasks:
        st.write(f"ID: {task['id']}, Name: {task['name']}, Start Date: {task['start_date']}, End Date: {task['end_date']}")
        st.write(f"Dependencies: {task['dependencies']}")
        st.write("---")

    with st.form("Create Task"):
        name = st.text_input("Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        dependencies = st.text_input("Dependencies")
        if st.form_submit_button("Create Task"):
            try:
                Task.create(name, start_date, end_date, dependencies)
                st.success("Task created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating task: {str(e)}")

def budget_management():
    st.subheader("Budget Management")
    budgets = Budget.get_all()
    for budget in budgets:
        st.write(f"ID: {budget['id']}, Project ID: {budget['project_id']}, Amount: {budget['amount']}")
        st.write(f"Date: {budget['date']}")
        st.write("---")

    with st.form("Create Budget"):
        project_id = st.number_input("Project ID", min_value=1)
        amount = st.number_input("Amount")
        date = st.date_input("Date")
        if st.form_submit_button("Create Budget"):
            try:
                Budget.create(project_id, amount, date)
                st.success("Budget created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating budget: {str(e)}")

def communication():
    st.subheader("Communication")
    messages = Message.get_all()
    for message in messages:
        st.write(f"From: {message['from_user']}, To: {message['to_user']}, Message: {message['content']}")
        st.write(f"Date: {message['date']}")
        st.write("---")

    with st.form("Send Message"):
        from_user = st.text_input("From")
        to_user = st.text_input("To")
        content = st.text_area("Message")
        date = st.date_input("Date")
        if st.form_submit_button("Send Message"):
            try:
                Message.create(from_user, to_user, content, date)
                st.success("Message sent successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error sending message: {str(e)}")

def reporting():
    st.subheader("Reporting")
    reports = Report.get_all()
    for report in reports:
        st.write(f"ID: {report['id']}, Name: {report['name']}, Content: {report['content']}")
        st.write(f"Date: {report['date']}")
        st.write("---")

    with st.form("Create Report"):
        name = st.text_input("Name")
        content = st.text_area("Content")
        date = st.date_input("Date")
        if st.form_submit_button("Create Report"):
            try:
                Report.create(name, content, date)
                st.success("Report created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error creating report: {str(e)}")

if __name__ == "__main__":
    main()
