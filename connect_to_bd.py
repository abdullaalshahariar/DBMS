#!/usr/bin/env python3
"""
Database Connection and Query Tool
This file provides functions to connect to MySQL database and execute queries.
"""

import mysql.connector
from mysql.connector import Error
import sys

# Database configuration (same as Flask app)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'flask',
    'database': 'donation'
}

def get_connection():
    """
    Create and return a database connection.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    """
    Execute a SQL query and return results.
    
    Args:
        query (str): SQL query to execute
        params (tuple): Parameters for the query (optional)
        fetch (bool): Whether to fetch results (True for SELECT, False for INSERT/UPDATE/DELETE)
    
    Returns:
        list: Query results if fetch=True, None otherwise
    """
    connection = get_connection()
    if not connection:
        return None
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            # For SELECT queries
            results = cursor.fetchall()
            print(f"✅ Query executed successfully. Found {len(results)} rows.")
            return results
        else:
            # For INSERT/UPDATE/DELETE queries
            connection.commit()
            print(f"✅ Query executed successfully. {cursor.rowcount} rows affected.")
            return cursor.rowcount
            
    except Error as e:
        print(f"❌ Error executing query: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

def show_all_tables():
    """Show all tables in the database."""
    query = "SHOW TABLES"
    results = execute_query(query)
    if results and isinstance(results, list):
        print("\n📋 Tables in database:")
        for row in results:
            print(f"  - {list(row.values())[0]}")
    return results

def show_table_structure(table_name):
    """Show structure of a specific table."""
    query = f"DESCRIBE {table_name}"
    results = execute_query(query)
    if results and isinstance(results, list):
        print(f"\n📋 Structure of table '{table_name}':")
        for row in results:
            print(f"  {row['Field']} | {row['Type']} | {row['Null']} | {row['Key']} | {row['Default']}")
    return results

def show_all_users():
    """Show all users in the user table."""
    query = "SELECT id, username, role FROM user"
    results = execute_query(query)
    if results and isinstance(results, list):
        print("\n👥 All users:")
        for user in results:
            print(f"  ID: {user['id']} | Username: {user['username']} | Role: {user['role']}")
    return results

def create_admin_user():
    """Create admin user with hashed password."""
    from werkzeug.security import generate_password_hash
    
    username = 'admin'
    password = 'Admin@1'
    role = 'admin'
    hashed_password = generate_password_hash(password)
    
    # Check if admin already exists
    check_query = "SELECT username FROM user WHERE username = %s"
    existing = execute_query(check_query, (username,))
    
    if existing:
        print("❌ Admin user already exists!")
        return False
    
    # Insert admin user
    insert_query = "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)"
    result = execute_query(insert_query, (username, hashed_password, role), fetch=False)
    
    if result:
        print("✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   Role: {role}")
        return True
    return False

def create_project_database():
    """Create a new 'project' database and grant permissions."""
    connection = get_connection()
    if not connection:
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS project")
        print("✅ Database 'project' created successfully!")
        
        # Grant permissions to flaskuser
        cursor.execute("GRANT ALL PRIVILEGES ON project.* TO 'flaskuser'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ Permissions granted to flaskuser for 'project' database!")
        
        connection.commit()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

def main():
    """Main function to demonstrate usage."""
    print("🔗 Database Connection Tool")
    print("=" * 50)
    
    # Test connection
    connection = get_connection()
    if not connection:
        print("❌ Cannot connect to database. Please check your configuration.")
        sys.exit(1)
    connection.close()
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Show all tables")
        print("2. Show table structure")
        print("3. Show all users")
        print("4. Create admin user")
        print("5. Create 'project' database")
        print("6. Execute custom query")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            show_all_tables()
        
        elif choice == '2':
            table_name = input("Enter table name: ").strip()
            if table_name:
                show_table_structure(table_name)
        
        elif choice == '3':
            show_all_users()
        
        elif choice == '4':
            create_admin_user()
        
        elif choice == '5':
            create_project_database()
        
        elif choice == '6':
            query = input("Enter SQL query: ").strip()
            if query:
                is_select = query.upper().startswith('SELECT') or query.upper().startswith('SHOW') or query.upper().startswith('DESCRIBE')
                execute_query(query, fetch=is_select)
        
        elif choice == '7':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
