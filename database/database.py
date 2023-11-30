import sqlite3
import time

import psycopg2

host = 'localhost'
user = 'postgres'
password = 'root'
db_name = 'bot-misha'

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

    def create_users_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users(
                telegram_id BIGINT PRIMARY KEY,
                username CHARACTER VARYING(50),
                gender CHARACTER VARYING(10),
                language CHARACTER VARYING(10),
                country CHARACTER VARYING(50),
                age SMALLINT,
                interests CHARACTER VARYING(20),
                location_latitude REAL,
                location_longitude REAL,
                date_of_registration BIGINT
            )
        '''
        self.manager(sql, commit=True)

    def drop_users_table(self):
        sql = '''
            DROP TABLE IF EXISTS users
        '''
        self.manager(sql, commit=True)

    def add_user(self, telegram_id, username, gender, language, country, age, interests, location_latitude,
                 location_longitude, date_of_registration):
        sql = '''
            INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        self.manager(sql, telegram_id, username, gender, language, country, age, interests,
                     location_latitude, location_longitude, date_of_registration, commit=True)

    def remove_user(self, telegram_id):
        sql = '''
            DELETE FROM users WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)


    def get_user(self, telegram_id):
        sql = '''
            SELECT * FROM users WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_users(self):
        sql = '''
            SELECT * FROM users
        '''
        return self.manager(sql, fetchall=True)

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

    def change_username_by_telegram_id(self, telegram_id, username):
        sql = '''
            UPDATE users SET username = %s WHERE telegram_id = %s
        '''
        self.manager(sql, username, telegram_id, commit=True)

    def change_gender_by_telegram_id(self, telegram_id, gender):
        sql = '''
            UPDATE users SET gender = %s WHERE telegram_id = %s
        '''
        self.manager(sql, gender, telegram_id, commit=True)

    def change_country_by_telegram_id(self, telegram_id, country):
        sql = '''
            UPDATE users SET country = %s WHERE telegram_id = %s
        '''
        self.manager(sql, country, telegram_id, commit=True)

    def change_age_by_telegram_id(self, telegram_id, age):
        sql = '''
            UPDATE users SET age = %s WHERE telegram_id = %s
        '''
        self.manager(sql, age, telegram_id, commit=True)

    def change_interests_by_telegram_id(self, telegram_id, interests):
        sql = '''
            UPDATE users SET interests = %s WHERE telegram_id = %s
        '''
        self.manager(sql, interests, telegram_id, commit=True)

    def change_location_by_telegram_id(self, telegram_id, latitude, longitude):
        sql = '''
            UPDATE users SET location_latitude = %s, location_longitude = %s WHERE telegram_id = %s
        '''
        self.manager(sql, latitude, longitude, telegram_id, commit=True)

    # -----------------------------users-----------------------------

    # -----------------------------users_stats-----------------------------
    def create_users_stats_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users_stats(
                telegram_id BIGINT PRIMARY KEY,
                rating BIGINT DEFAULT 0,
                likes BIGINT DEFAULT 0,
                dislikes BIGINT DEFAULT 0,
                sent_messages BIGINT DEFAULT 0,
                sent_photos BIGINT DEFAULT 0,
                sent_videos BIGINT DEFAULT 0,
                sent_videos_note BIGINT DEFAULT 0,
                sent_stickers BIGINT DEFAULT 0,
                sent_voices BIGINT DEFAULT 0,
                sent_audios BIGINT DEFAULT 0,
                sent_document BIGINT DEFAULT 0,
                time_spent_in_chatting BIGINT DEFAULT 0
            )
        '''
        self.manager(sql, commit=True)

    def drop_users_stats(self):
        sql = '''
            DROP TABLE IF EXISTS users_stats
        '''
        self.manager(sql, commit=True)
    def add_user_stats(self, telegram_id):
        sql = '''
            INSERT INTO users_stats(telegram_id) VALUES(%s)
        '''
        self.manager(sql, telegram_id, commit=True)

    def remove_user_stats(self, telegram_id):
        sql = '''
            DELETE FROM users_stats WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)

    def get_user_stats(self, telegram_id):
        sql = '''
            SELECT * FROM users_stats WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def change_user_stats(self, telegram_id, rating=0, likes=0, dislikes=0, sent_messages=0, sent_photos=0,
                          sent_videos=0, sent_videos_note=0, sent_stickers=0, sent_voices=0, sent_audios=0,
                          sent_document=0, time_spent_in_chatting=0):
        sql = '''
            UPDATE users_stats 
            SET rating = rating + %s,
                likes = likes + %s,
                dislikes = dislikes + %s,
                sent_messages = sent_messages + %s,
                sent_photos = sent_photos + %s,
                sent_videos = sent_videos + %s,
                sent_videos_note = sent_videos_note + %s,
                sent_stickers = sent_stickers + %s,
                sent_voices = sent_voices + %s,
                sent_audios = sent_audios + %s,
                sent_document = sent_document + %s,
                time_spent_in_chatting = time_spent_in_chatting + %s
            WHERE telegram_id = %s
        '''
        self.manager(sql, rating, likes, dislikes, sent_messages, sent_photos, sent_videos,
                     sent_videos_note, sent_stickers, sent_voices, sent_audios, sent_document,
                     time_spent_in_chatting, telegram_id, commit=True)

    def get_user_to_profile(self, telegram_id):
        sql = '''
            SELECT 
                users_stats.likes,
                users_stats.dislikes,
                users_stats.rating,
                
                users.gender,
                users.country,
                users.language,
                users.age,
                users.interests,
                users.location_latitude,
                users.location_longitude,
                
                users_stats.sent_messages,
                users_stats.sent_photos,
                users_stats.sent_videos,
                users_stats.sent_videos_note,
                users_stats.sent_stickers,
                users_stats.sent_voices,
                users_stats.sent_audios,
                users_stats.sent_document,
                
                users_stats.time_spent_in_chatting,
                users.date_of_registration

            FROM users_stats
            JOIN users ON users_stats.telegram_id = users.telegram_id
            WHERE users_stats.telegram_id = %s
                
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    # -----------------------------users_stats-----------------------------

    # -----------------------------premium-----------------------------
    def create_premium_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS premium(
                telegram_id BIGINT PRIMARY KEY,
                from_date BIGINT,
                to_date BIGINT
            )
        '''
        self.manager(sql, commit=True)

    def drop_premium_table(self):
        sql = '''
            DROP TABLE IF EXISTS premium
        '''
        self.manager(sql, commit=True)

    def add_premium(self, telegram_id, from_date, to_date):
        sql = '''
            INSERT INTO premium VALUES(%s,%s,%s)
        '''
        self.manager(sql, telegram_id, from_date, to_date, commit=True)

    def get_premium(self, telegram_id):
        sql = '''
            SELECT * FROM premium WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_overdue_premium(self, telegram_id, time):
        sql = '''
            SELECT * FROM premium WHERE telegram_id = %s AND to_date < %s
        '''
        return self.manager(sql, telegram_id, time, fetchone=True)

    def remove_premium(self, telegram_id):
        sql = '''
            DELETE FROM premium WHERE telegram_id = %s
        '''
        self.manager(sql, telegram_id, commit=True)

    # -----------------------------premium-----------------------------

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

    def get_user_from_chatting(self, telegram_id):
        sql = '''
            SELECT * FROM in_chatting WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_users_from_chatting(self):
        sql = '''
            SELECT * FROM in_chatting
        '''
        return self.manager(sql, fetchall=True)





    def create_test(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS test(
                telegram_id BIGINT PRIMARY KEY,
                what SMALLINT 
            )
        '''
        self.manager(sql, commit=True)

    def drop_test(self):
        sql = '''
            DROP TABLE IF EXISTS test
        '''
        self.manager(sql, commit=True)

    def add_test(self, telegram_id, what):
        sql = '''
            INSERT INTO test VALUES(%s,%s)
        '''
        self.manager(sql, telegram_id, what, commit=True)

    def get_test(self, telegram_id):
        sql = '''
            SELECT * FROM test WHERE telegram_id = %s
        '''
        return self.manager(sql, telegram_id, fetchone=True)





















