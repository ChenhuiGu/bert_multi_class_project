from utils.MySQLEngine import MySQLEngine
from utils.srf_log import logger
import config


class DBInterface:
    def __init__(self):
        self.database = MySQLEngine()
        self.database.connect(db_host=config.mysql_host,
                              db_user=config.mysql_user,
                              db_pwd=config.mysql_pwd,
                              db=config.mysql_db)
        logger.info(f'DBInterface init')


def _init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


def get_keys():
    if '_global_dict' not in locals().keys():
        return []
    return _global_dict.keys()


def load_dbinterface():
    _global_dict['dbinterface'] = DBInterface()


def init_load():
    load_dbinterface()


if __name__ == "__main__":
    _init()
    load_dbinterface()
