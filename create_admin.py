#!/usr/bin/env python3

from werkzeug.security import generate_password_hash
import mysql.connector

# Admin credentials
username = 'admin'
password = 'Admin@1'
role = 'admin'

# Generate hashed password
hashed_password = generate_password_hash(password)

print("="*50)
print("ADMIN USER CREATION")
print("="*50)
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Role: {role}")
print(f"Hashed Password: {hashed_password}")
print()

# SQL command
sql_command = f"INSERT INTO user (username, password, role) VALUES ('{username}', '{hashed_password}', '{role}');"
print("SQL Command to run in MySQL:")
print("-" * 30)
print(sql_command)
print()

# Option to insert directly into database
try_direct = input("Do you want to try inserting directly into the database? (y/n): ")

if try_direct.lower() == 'y':
    try:
        # Database connection (using same config as Flask app)
        db = mysql.connector.connect(
            host='localhost',
            user='flaskuser',
            password='flask',
            database='donation'
        )
        cursor = db.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT username FROM user WHERE username = %s", (username,))
        existing = cursor.fetchone()
        
        if existing:
            print("❌ Admin user already exists!")
        else:
            # Insert admin user
            cursor.execute("INSERT INTO user (username, password, role) VALUES (%s, %s, %s)", 
                         (username, hashed_password, role))
            db.commit()
            print("✅ Admin user created successfully!")
            
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("Copy the SQL command above and run it in your MySQL client.")
