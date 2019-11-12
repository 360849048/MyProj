from app import sqljob
from app.pathinfo import *


t_soft = sqljob.TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH)

print(t_soft.conn_pool)
