

import pymysql as sql
import os

from font_import import *
from Class.customException import *

def connect_to_database():
    """Fonction essayant d'établir une connecion avec la base

    Returns:
        retourne une connexion sql ou None si la connexion a échoué
    """
    try:
        conn = sql.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('SQL_MOT_DE_PASSE'),
            database=os.environ.get('DB_NAME'),
            autocommit=True,collation="utf8mb4_unicode_ci"
            )
        conn.ping(False)
        return conn
    except Exception as e:
        return None
    

            
            
