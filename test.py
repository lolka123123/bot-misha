from data.loader import db

# import psycopg2
#
# host = 'localhost'
# user = 'postgres'
# password = 'root'
# db_name = 'bot-misha'
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
#         return self.manager(sql, fetchone=True)
#
# print(DataBase().test())

