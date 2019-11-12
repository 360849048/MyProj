from app.abstractsqlpool import AbstractConnPool
from app.pathinfo import *


class SoftDbCoonPool(AbstractConnPool):
    db_path = SOFTWARE_VERSION_INFO_DB_PATH


class IoDbConnPool(AbstractConnPool):
    db_path = IO_INFO_DB_PATH
    MIN_CONN = 6
    MAX_CONN = 12


class UserDbCoonPool(AbstractConnPool):
    db_path = USER_INFO_DB_PATH


class LogDbCoonPool(AbstractConnPool):
    db_path = LOG_DB_PATH


class ReleaseNoteDbCoonPool(AbstractConnPool):
    db_path = STD_SOFTWARE_RELEASE_NOTE_DB_PATH


def getCoonPool(db_path):
    # Factory method
    if db_path == SOFTWARE_VERSION_INFO_DB_PATH:
        return SoftDbCoonPool()
    elif db_path == IO_INFO_DB_PATH:
        return IoDbConnPool()
    elif db_path == USER_INFO_DB_PATH:
        return UserDbCoonPool()
    elif db_path == LOG_DB_PATH:
        return LogDbCoonPool()
    elif db_path == STD_SOFTWARE_RELEASE_NOTE_DB_PATH:
        return ReleaseNoteDbCoonPool()
    else:
        return None


