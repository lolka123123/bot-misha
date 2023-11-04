import sqlite3
import time

import psycopg2

host = 'localhost'
user = 'postgres'
password = 'root'
db_name = 'bot-misha'

# class DataBase:
#     def __init__(self):
#         self.database = psycopg2.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=db_name
#         )
#
#     def manager(self, sql, *args,
#                 fetchone: bool = False,
#                 fetchall: bool = False,
#                 commit: bool = False):
#         with self.database as db:
#             with db.cursor() as cursor:
#                 cursor.execute(sql, args)
#                 if commit:
#                     result = db.commit()
#                 if fetchone:
#                     result = cursor.fetchone()
#                 if fetchall:
#                     result = cursor.fetchall()
#                 return result

# class DataBase:
#     def __init__(self):
#         self.database = sqlite3.connect('db.sqlite3', check_same_thread=False)
#
#     def manager(self, sql, *args,
#                 fetchone: bool = False,
#                 fetchall: bool = False,
#                 commit: bool = False):
#         with self.database as db:
#             cursor = db.cursor()
#             cursor.execute(sql, args)
#             if commit:
#                 result = db.commit()
#             if fetchone:
#                 result = cursor.fetchone()
#             if fetchall:
#                 result = cursor.fetchall()
#             return result


class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    result = db.commit()
                if fetchone:
                    result = cursor.fetchone()
                if fetchall:
                    result = cursor.fetchall()
                return result
    # -----------------------------users-----------------------------

    def create_users_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users(
                telegram_id BIGINT PRIMARY KEY,
                username CHARACTER VARYING(50),
                gender CHARACTER VARYING(10),
                language CHARACTER VARYING(10)
            )
        '''
        self.manager(sql, commit=True)

    def drop_users_table(self):
        sql = '''
            DROP TABLE IF EXISTS users
        '''
        self.manager(sql, commit=True)

    def add_user(self, telegram_id, username, gender, language):
        sql = '''
            INSERT INTO users VALUES (%s,%s,%s,%s)
        '''
        self.manager(sql, telegram_id, username, gender, language, commit=True)


    def get_user(self, telegram_id):
        sql = '''
            SELECT * FROM users WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_user_by_username(self, username):
        sql = '''
            SELECT * FROM users WHERE username = %s
        '''
        return self.manager(sql, username, fetchone=True)

    def change_user_language_by_telegram_id(self, telegram_id, language):
        sql = '''
            UPDATE users SET language = %s WHERE telegram_id = %s
        '''
        self.manager(sql, language, telegram_id, commit=True)

    # -----------------------------users-----------------------------
    # -----------------------------admin_list-----------------------------

    def create_admin_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS admin_list(
                telegram_id BIGINT PRIMARY KEY,
                level_access INTEGER
            )
        '''
        self.manager(sql, commit=True)

    def drop_admin_table(self):
        sql = '''
            DROP TABLE IF EXISTS admin_list
        '''
        self.manager(sql, commit=True)

    def add_admin(self, telegram_id, level_access):
        sql = '''
            INSERT INTO admin_list VALUES(%s,%s)
        '''
        self.manager(sql, telegram_id, level_access, commit=True)

    def delete_admin(self, telegram_id):
        sql = '''
            DELETE FROM admin_list WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)

    def get_admin(self, telegram_id):
        sql = '''
            SELECT * FROM admin_list WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    # -----------------------------admin_list-----------------------------
    # -----------------------------ban_list-----------------------------


    def create_ban_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS ban_list(
                telegram_id BIGINT PRIMARY KEY,
                date BIGINT,
                to_date BIGINT,
                who_banned CHARACTER VARYING(50),
                reason CHARACTER VARYING(100)
            )
        '''
        self.manager(sql, commit=True)

    def drop_ban_table(self):
        sql = '''
            DROP TABLE IF EXISTS ban_list
        '''
        self.manager(sql, commit=True)

    def add_user_to_ban(self, telegram_id, date, to_date, who_banned, reason):
        sql = '''
            INSERT INTO ban_list VALUES(%s,%s,%s,%s,%s)
        '''
        self.manager(sql, telegram_id, date, to_date, who_banned, reason, commit=True)

    def get_banned_user(self, telegram_id):
        sql = '''
            SELECT * FROM ban_list WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_banned_users(self):
        sql = '''
            SELECT * FROM ban_list
        '''
        return self.manager(sql, fetchall=True)

    def remove_ban_user(self, telegram_id):
        sql = '''
            DELETE FROM ban_list WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)


    # -----------------------------ban_list-----------------------------
    # -----------------------------in_searching-----------------------------

    def create_in_searching_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS in_searching(
                telegram_id BIGINT PRIMARY KEY,
                date BIGINT
            )
        '''
        self.manager(sql, commit=True)

    def drop_in_searching_table(self):
        sql = '''
            DROP TABLE IF EXISTS in_searching
        '''
        self.manager(sql, commit=True)

    def add_user_in_searching(self, telegram_id, date):
        sql = '''
            INSERT INTO in_searching VALUES(%s,%s)
        '''
        self.manager(sql, telegram_id, date, commit=True)

    def remove_user_from_searching(self, telegram_id):
        sql = '''
            DELETE FROM in_searching WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)

    def remove_all_users_from_searching(self):
        sql = '''
            DELETE FROM in_searching
        '''
        self.manager(sql, commit=True)

    def get_users_from_searching(self):
        sql = '''
            SELECT * FROM in_searching
        '''
        return self.manager(sql, fetchall=True)

    def get_users_from_searching_after_seconds(self, date):
        sql = '''
            SELECT * FROM in_searching WHERE date <= %s
        '''
        return self.manager(sql, date-3, fetchall=True)

    def get_user_from_searching(self, telegram_id):
        sql = '''
            SELECT * FROM in_searching WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    # -----------------------------in_searching-----------------------------
    # -----------------------------chats-----------------------------
    def create_chats_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS chats(
                id SERIAL PRIMARY KEY,
                first_telegram_id BIGINT,
                second_telegram_id BIGINT,
                date BIGINT
            )
        '''
        self.manager(sql, commit=True)

    def drop_chats_table(self):
        sql = '''
            DROP TABLE IF EXISTS chats
        '''
        self.manager(sql, commit=True)




    def add_chat(self, first_telegram_id, second_telegram_id, date):
        sql = '''
            INSERT INTO chats(first_telegram_id, second_telegram_id, date) VALUES(%s,%s,%s)
        '''
        self.manager(sql, first_telegram_id, second_telegram_id, date, commit=True)

    def get_last_chat(self):
        sql = '''
            SELECT * FROM chats ORDER BY id DESC LIMIT 1
        '''
        return self.manager(sql, fetchone=True)


    def create_chat_messages_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS chat_messages(
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                telegram_id BIGINT,
                message_text CHARACTER VARYING(255),
                date BIGINT
            )
        '''
        self.manager(sql, commit=True)

    def drop_chat_messages_table(self):
        sql = '''
            DROP TABLE IF EXISTS chat_messages
        '''
        self.manager(sql, commit=True)

    def add_chat_message(self, chat_id, telegram_id, message_text, date):
        sql = '''
            INSERT INTO chat_messages(chat_id, telegram_id, message_text, date) VALUES(%s,%s,%s,%s)
        '''
        self.manager(sql, chat_id, telegram_id, message_text, date, commit=True)

    def create_in_chatting_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS in_chatting(
                telegram_id BIGINT PRIMARY KEY, 
                chat_id BIGINT
            )
        '''
        self.manager(sql, commit=True)



    def drop_in_chatting_table(self):
        sql = '''
            DROP TABLE IF NOT EXISTS in_chatting
        '''
        self.manager(sql, commit=True)

    def remove_all_users_from_chatting(self):
        sql = '''
            DELETE FROM in_chatting
        '''
        self.manager(sql, commit=True)

    def remove_user_from_chatting(self, telegram_id):
        sql = '''
            DELETE FROM in_chatting WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)

    def add_in_chatting(self, telegram_id, chat_id):
        sql = '''
            INSERT INTO in_chatting VALUES(%s, %s)
        '''
        self.manager(sql, telegram_id, chat_id, commit=True)

    def get_users_from_chatting(self):
        sql = '''
            SELECT * FROM in_chatting
        '''
        return self.manager(sql, fetchall=True)


