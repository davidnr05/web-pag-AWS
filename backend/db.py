import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="sakila-db.cbsiguw8kcda.us-east-1.rds.amazonaws.com",      # ← sin "https://", solo el endpoint
        user="admin",
        password="admin123",
        database="sakila"
    )
