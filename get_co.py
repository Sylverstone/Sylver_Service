import os
import pymysql as sql

try:
    connection_principale = sql.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('SQL_MOT_DE_PASSE'),
        database=os.environ.get('DB_NAME'),
        autocommit=True,collation="utf8mb4_unicode_ci"
        )
    connection_principale.ping(False)
except Exception as e:
    connection_principale = None