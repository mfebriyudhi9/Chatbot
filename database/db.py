import mysql.connector
from mysql.connector import Error
import os
import logging

class DataBase:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        self.connect_timeout = 10

        self.create_table_query = """
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_message TEXT NOT NULL,
                bot_message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id VARCHAR(36) NOT NULL
            );"""

        self.insert_chat_query = """
            INSERT INTO conversation_history 
            (user_message, bot_message, user_id) 
            VALUES (%s, %s, %s);"""

        self.retrieve_chat_query = """
            SELECT user_message, bot_message 
            FROM conversation_history 
            WHERE user_id = %s 
            ORDER BY timestamp DESC LIMIT %s;"""

        # Configure logging
        logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

    def connect_to_db(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                connect_timeout=self.connect_timeout,
                charset="utf8mb4"
            )
        except Error as e:
            logging.error(f"Error connecting to the database: {e}")
            return None

    def execute_query(self, query, params=None, fetch=False):
        connection = self.connect_to_db()
        if not connection:
            return None if fetch else False

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                connection.commit()
        except Error as e:
            logging.error(f"Error executing query: {e}")
            return None if fetch else False
        finally:
            connection.close()

    def create_table_if_not_exists(self):
        self.execute_query(self.create_table_query)

    def save_to_database(self, user_message, bot_message, user_id):
        self.execute_query(self.insert_chat_query, (user_message, bot_message, user_id))

    def retrieve_chat_history(self, user_uuid, limit):
        history = self.execute_query(self.retrieve_chat_query, (user_uuid, limit), fetch=True)
        if history:
            return "\n".join([f"user: {user_msg} \nBot: {bot_resp}" for user_msg, bot_resp in reversed(history)])
        return ""
