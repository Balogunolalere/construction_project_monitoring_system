import sqlite3
from datetime import date

def get_conn():
    return sqlite3.connect('construction_projects.db')

def test_create_project():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Projects (name, description, start_date, end_date)
        VALUES (?, ?, ?, ?)
    """, ("Test Project", "This is a test project", date.today(), date.today()))
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"Created project with ID: {project_id}")
    return project_id

def test_read_project(project_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    conn.close()
    print(f"Read project: {project}")

def test_update_project(project_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Projects 
        SET name = ?, description = ?, start_date = ?, end_date = ?
        WHERE id = ?
    """, ("Updated Test Project", "This project has been updated", date.today(), date.today(), project_id))
    conn.commit()
    conn.close()
    print(f"Updated project with ID: {project_id}")

def test_delete_project(project_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    print(f"Deleted project with ID: {project_id}")

if __name__ == "__main__":
    # Test create
    project_id = test_create_project()
    
    # Test read
    test_read_project(project_id)
    
    # Test update
    test_update_project(project_id)
    test_read_project(project_id)
    
    # Test delete
    test_delete_project(project_id)
    test_read_project(project_id)