import mysql.connector
import bcrypt
from config import DB_CONFIG

DB_TABLES = {
    'traffic_data': """
        CREATE TABLE IF NOT EXISTS traffic_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            direction ENUM('North', 'East', 'South', 'West') NOT NULL,
            vehicle_count INT NOT NULL,
            ambulance_count INT NOT NULL,
            avg_speed FLOAT,
            congestion_index FLOAT,
            vehicle_types JSON,
            positions JSON
        )
    """,
    'users': """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'officer') NOT NULL
        )
    """,
    'signal_changes': """
        CREATE TABLE IF NOT EXISTS signal_changes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            direction ENUM('North', 'East', 'South', 'West') NOT NULL,
            green_time INT NOT NULL,
            mode ENUM('normal', 'emergency') NOT NULL
        )
    """,
    'emergencies': """
        CREATE TABLE IF NOT EXISTS emergencies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trigger_time DATETIME NOT NULL,
            override_time DATETIME NOT NULL,
            direction ENUM('North', 'East', 'South', 'West') NOT NULL,
            active_duration INT NOT NULL
        )
    """
}

def create_db_connection():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        return None

def setup_database():
    """Create database and tables if they don't exist"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor(buffered=True)

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        for table, ddl in DB_TABLES.items():
            cursor.execute(ddl)
            cursor.fetchall()
            print(f"Created table {table} successfully")

        password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT IGNORE INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("admin", password.decode(), "admin")
        )
        conn.commit()
        print("Database setup completed successfully")

    except mysql.connector.Error as err:
        print(f"Database setup failed: {err}")
        exit(1)
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def create_user(username, password, role):
    conn = create_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"User {username} already exists")
            return True

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_pw.decode(), role)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"User creation failed: {err}")
        return False
    finally:
        cursor.close()
        conn.close()