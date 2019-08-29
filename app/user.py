from uuid import uuid4
import hmac
import sqlite3
from app.pathinfo import *
from app.log import log


'''
    数据库初始状态
    账号：admin,
    密码：12345
    这个账号的id为1，并以此id作为管理员权限的标志。其余账号只有普通权限
'''


def verifyAccount(account, password):
    ret = {'status': False, 'username': None, 'admin': False}
    conn = sqlite3.connect(USER_INFO_DB_PATH)
    c = conn.cursor()
    sql = "SELECT account, id, username, password_md5, uuid FROM " + ACCOUNT_TABLE_NAME + " WHERE account=%r" % account
    c.execute(sql)
    user_info = c.fetchone()
    if user_info:
        user_id, username, pwd_md5, salt = user_info[1:]

        h = hmac.new(salt.encode(), password.encode(), digestmod='MD5')
        pwd_to_md5 = h.hexdigest()

        ret['status'] = pwd_to_md5 == pwd_md5
        ret['username'] = username
        ret['admin'] = user_id == 1

    conn.close()
    return ret


def createAccount(account, password, username):
    ret = False
    salt = str(uuid4())
    h = hmac.new(salt.encode(), password.encode(), digestmod="MD5")
    password_md5 = h.hexdigest()

    conn = sqlite3.connect(USER_INFO_DB_PATH)
    c = conn.cursor()
    sql = "INSERT INTO " + ACCOUNT_TABLE_NAME + "(account, password_md5, uuid, username) VALUES (%r, %r, %r, %r)" % \
          (account, password_md5, salt, username)
    try:
        c.execute(sql)
        conn.commit()
        ret = True
    except Exception as e:
        print(e)
        log.record(str(e))

    conn.close()
    return ret


def modifyPwd(account, new_password):
    ret = False
    conn = sqlite3.connect(USER_INFO_DB_PATH)
    c = conn.cursor()
    sql = "SELECT account, uuid FROM " + ACCOUNT_TABLE_NAME + " WHERE account = %r" % account
    c.execute(sql)
    user_info = c.fetchone()

    if user_info:
        account, salt = user_info
        h = hmac.new(salt.encode(), new_password.encode(), digestmod='MD5')
        new_password_md5 = h.hexdigest()
        sql = "UPDATE " + ACCOUNT_TABLE_NAME + " SET password_md5=%r" % new_password_md5 + " WHERE account=%r" % account
        try:
            c.execute(sql)
            conn.commit()
            ret = True
        except Exception as e:
            print(e)
            log.record(str(e))

    conn.close()
    return ret


def deleteAccount(account):
    ret = False
    conn = sqlite3.connect(USER_INFO_DB_PATH)
    c = conn.cursor()
    sql = "DELETE FROM " + ACCOUNT_TABLE_NAME + " WHERE account=%r" % account
    try:
        c.execute(sql)
        conn.commit()
        ret = True
    except Exception as e:
        print(e)
        log.record(str(e))

    conn.close()
    return ret


def modifyUsername(account, new_username):
    ret = False
    conn = sqlite3.connect(USER_INFO_DB_PATH)
    c = conn.cursor()
    sql = "SELECT account FROM " + ACCOUNT_TABLE_NAME + " WHERE account = %r" % account
    c.execute(sql)
    user_info = c.fetchone()

    if user_info:
        account, = user_info
        sql = "UPDATE " + ACCOUNT_TABLE_NAME + " SET username=%r" % new_username + " WHERE account=%r" % account
        try:
            c.execute(sql)
            conn.commit()
            ret = True
        except Exception as e:
            print(e)
            log.record(str(e))

    conn.close()
    return ret
