import os
import pymysql as sql
import dotenv

dotenv.load_dotenv(override=True)

try:
    connection_principale = sql.connect(
        host=os.environ.get('HOST'),
        user=os.environ.get('USER'),
        password=os.environ.get('SQL_MOT_DE_PASSE'),
        database=os.environ.get('DB_NAME'),
        autocommit=True,collation="utf8mb4_unicode_ci"
        )
    connection_principale.ping(False)
    print("La connection a été initialisé")
except Exception as e:
    print("la connexion n'a pas été initilisé")
    connection_principale = None