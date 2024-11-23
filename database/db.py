import mysql.connector
from mysql.connector import Error
import os

class DataBase:
    def __init__(self):
        try:
            self.host = os.getenv("MYSQL_HOST")
            self.user = os.getenv("MYSQL_USER")
            self.password = os.getenv("MYSQL_PASSWORD")
            self.database = os.getenv("MYSQL_DATABASE")
            self.connect_timeout = 10

            self.create_table_query = """
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_massage TEXT NOT NULL,
                    bot_massage TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id VARCHAR(36) NOT NULL
                );"""
            
            self.insert_chat_query = """
                INSERT INTO conversation_history 
                (user_massage, bot_massage, user_id) 
                VALUES (%s, %s, %s);"""
            
            self.retrieve_chat_query = """
                SELECT user_massage, bot_massage 
                FROM conversation_history 
                WHERE user_id = %s 
                ORDER BY timestamp DESC LIMIT %s;"""
            
            self.connection = self.connect_to_db()
        
        except Error as e:
            print(f"Error during initialization: {e}")
            self.connection = None

    def connect_to_db(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                connect_timeout=self.connect_timeout
            )
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def create_table_if_not_exists(self):
        if not self.connection:
            print("No database connection.")
            return

        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.create_table_query)
                connection.commit()
        except Error as e:
            print(f"Error creating table: {e}")

    def save_to_database(self, user_massage, bot_massage, user_id):
        if not self.connection:
            print("No database connection.")
            return

        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.insert_chat_query, (user_massage, bot_massage, user_id))
                connection.commit()
        except Error as e:
            print(f"Error saving chat to database: {e}")

    def retrieve_chat_history(self, user_uuid, limit):
        if not self.connection:
            print("No database connection.")
            return ""

        try:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(self.retrieve_chat_query, (user_uuid, limit))
                    history = cursor.fetchall()

            if history:
                formatted_history = "\n".join([f"user: {user_msg} \nBot: {bot_resp}" for user_msg, bot_resp in reversed(history)])
            else:
                formatted_history = ""

            return formatted_history
        
        except Error as e:
            print(f"Error retrieving chat history: {e}")
            return ""
