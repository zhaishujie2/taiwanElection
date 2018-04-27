# coding=utf-8
import hashlib

import pymysql

from .config import mysql_charset,mysql_db,mysql_host,mysql_passwd,mysql_port,mysql_user


def getconn():
    conn = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        passwd=mysql_passwd,
        db=mysql_db,
        charset=mysql_charset
    )
    return conn


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

def closeAll(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

