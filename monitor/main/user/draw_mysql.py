# coding=utf-8
from monitor.util.mysql_util import getconn,md5,closeAll
from monitor import app

# 登录界面
def login(name, password):
    conn = getconn()
    cur= conn.cursor()
    try:
            password = md5(password)
            sql = "select * from users where user=%s and passwd=%s"
            result = cur.execute(sql, (name, password))
            return result
    except (Exception) as e:
        app.logger.error(e)
        return "0"
    finally:
        closeAll(conn,cur)
