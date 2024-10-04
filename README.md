# Construction Project Monitoring System

## Overview
The Construction Project Monitoring System is a web application built using Streamlit, a Python library for creating interactive web applications. This system allows users to manage construction projects, tasks, resources, and files, as well as handle user authentication and notifications.

## Features
1. **Project Management**:
   - Create, update, and delete construction projects.
   - View detailed information about projects, including start and end dates, description, and associated tasks, resources, and files.

2. **Task Management**:
   - Create, update, and delete tasks for each project.
   - Track task status (Not Started, In Progress, Completed).
   - View tasks associated with specific projects.

3. **Resource Management**:
   - Create, update, and delete resources, such as equipment or materials.
   - Track resource availability by setting available from and to dates.
   - View all available resources.

4. **File Management**:
   - Upload, update, and delete files associated with specific projects.
   - Track file versions and the user who uploaded each version.
   - View all files for a given project.

5. **User Management**:
   - Create, update, and delete user accounts.
   - Assign user roles (admin or user).
   - Restrict certain actions based on user roles (e.g., only admins can manage users).

6. **Notification System**:
   - Notify users of new projects, tasks, resources, and files created.
   - Notify users of updates to projects, tasks, resources, and files.
   - View all notifications for the logged-in user.

7. **Authentication**:
   - Users can log in and log out of the system.
   - New users can register for an account.

## Technologies Used
- **Python**: The primary programming language used for the backend logic.
- **Streamlit**: A Python library used for creating the interactive web application.
- **SQLite**: A lightweight, file-based database used for storing project, task, resource, file, and user data.
- **bcrypt**: A library used for hashing and storing user passwords securely.

## Installation and Setup
1. Clone the repository:
   ```
   git clone https://github.com/username/construction-project-monitoring-system.git
   ```

2. Change to the project directory:
   ```
   cd construction-project-monitoring-system
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

6. The application should now be running and accessible in your web browser at `http://localhost:8501`.

## Usage
1. When you first run the application, it will create an initial admin user with the following credentials:
   - Username: `admin`
   - Password: `admin`

2. Log in using the admin credentials.

3. Explore the different features of the application, such as managing projects, tasks, resources, files, and users.

4. You can create additional user accounts and assign them the "admin" or "user" role.

5. Users with the "admin" role can perform all actions, including managing other users.

6. Users with the "user" role can perform actions related to projects, tasks, resources, and files, but cannot manage other users.

7. The notification system will keep you informed of any changes made to the system.

## Database Schema
The application uses a SQLite database with the following tables:

1. **Projects**:
   - `id`: Unique identifier for the project
   - `name`: Name of the project
   - `description`: Description of the project
   - `start_date`: Start date of the project
   - `end_date`: End date of the project

2. **Tasks**:
   - `id`: Unique identifier for the task
   - `project_id`: Foreign key referencing the `id` column in the `Projects` table
   - `name`: Name of the task
   - `description`: Description of the task
   - `start_date`: Start date of the task
   - `end_date`: End date of the task
   - `status`: Status of the task (Not Started, In Progress, Completed)

3. **Resources**:
   - `id`: Unique identifier for the resource
   - `name`: Name of the resource
   - `type`: Type of the resource
   - `available_from`: Date the resource becomes available
   - `available_to`: Date the resource is no longer available

4. **Files**:
   - `id`: Unique identifier for the file
   - `project_id`: Foreign key referencing the `id` column in the `Projects` table
   - `name`: Name of the file
   - `file_path`: Path to the file on the server
   - `version`: Version number of the file
   - `uploaded_by`: Username of the user who uploaded the file
   - `uploaded_at`: Timestamp of when the file was uploaded

5. **Users**:
   - `id`: Unique identifier for the user
   - `username`: Username of the user
   - `password`: Hashed password of the user
   - `role`: Role of the user (admin or user)

6. **Notifications**:
   - `id`: Unique identifier for the notification
   - `user_id`: Foreign key referencing the `id` column in the `Users` table
   - `project_id`: Foreign key referencing the `id` column in the `Projects` table
   - `message`: Text of the notification
   - `sent_at`: Timestamp of when the notification was sent

## Error Handling and Logging
The application uses Python's built-in `logging` module to handle errors and log relevant information. The log file is named `app.log` and is stored in the same directory as the `app.py` file.

## Future Improvements
- **User Interface Enhancements**: Improve the overall user interface and user experience, including better layout, styling, and responsiveness.
- **Advanced Reporting and Analytics**: Implement more advanced reporting and analytics features, such as project progress tracking, resource utilization, and historical data analysis.
- **Integration with External Systems**: Explore the possibility of integrating the system with other construction management tools or enterprise software.
- **Mobile Accessibility**: Ensure the application is accessible and usable on mobile devices.
- **Improved Notifications**: Implement more advanced notification features, such as email or push notifications, to keep users informed of updates.
- **Access Control and Permissions**: Enhance the user management system to provide more granular access control and permissions.

