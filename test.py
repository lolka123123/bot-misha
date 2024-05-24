from data.loader import db

db.remove_premium(434874523)

# import psycopg2
#
# host = '83.69.139.168'
# user = 'anonimch_pg-user'
# password = '=Bd2WhnFbzbl'
# db_name = 'anonimch_bot-misha'
#
# # host = 'localhost'
# # user = 'postgres'
# # password = 'root'
# # db_name = 'bot-misha'
#
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
#
#     def test(self):
#         sql = '''
#             SELECT * FROM users
#         '''
#         return self.manager(sql, fetchall=True)
#
# print(DataBase().test())



# users = db.get_users()
# db.drop_users_table()
# db.create_users_table()
#
# for user in users:
#     db.add_user(user[0], user[1], user[2], user[3], 'uzbekistan', 0, 'communication', 0, 0, 1701191242)
#
# print(db.get_users())


# db.remove_user(434874523)
# print(db.get_users())

# users = db.get_users()
# for user in users:
#     db.add_user_stats(user[0])

# print(db.get_user_to_profile(434874523))

# db.add_premium(434874523, 1701281552, 1701281552+120)


# db.remove_user(434874523)
# db.remove_user_stats(434874523)