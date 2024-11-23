import mysql.connector

import os

class DataBase:
    def __init__(self):
        self.host=os.getenv("MYSQL_HOST"),
        self.user=os.getenv("MYSQL_USER"),
        self.password=os.getenv("MYSQL_PASSWORD"),
        self.database=os.getenv("MYSQL_DATABASE")
        self.connect_timeout=10

        self.create_table_query="""
                CREAT TABLE IF NOT EXISTS conversation_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_massage TEXT NOT NULL,
                    bot_massage TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id VARCHAR(36) NOT NULL
                );"""
        
        self.insert_chat_query = """INSERT INTO conversation_history "
                                    (user_massage, bot_massage, user_id) 
                                    VALUES (%s, %s, %s);"""
        
        self.retrieve_chat_query = """SELECT usr_massage, bot_massage 
                                      FROM conversation_history 
                                      WHERE user_uuid = %s 
                                      ORDER BY timestamp    
                                      DESC LIMIT %s;"""
        
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            connect_timeout=self.connect_timeout
        )
        
    def creat_table_if_not_exists(self):
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.create_table_query)
            connection.commit()

    def save_to_database(self, user_massage, bot_massage, user_id):
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.insert_chat_query, (user_massage, bot_massage, user_id))
            connection.commit()

    def retrieve_chat_history(self, user_uuid, limit):
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(self.retrieve_chat_query, (user_uuid, limit))
                history = cursor.fetchall()

        if history:
            formatted_history = "\n".join([f"user: {user_msg} \nBot: {bot_resp}" for user_msg, bot_resp in reversed(history)])
        else:
            formatted_history = ""

        return formatted_history