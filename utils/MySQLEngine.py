#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import pymysql
from dbutils.pooled_db import PooledDB
from utils.srf_log import logger

class MySQLEngine(object):
    '''
    mysql engine
    '''
    __tablename__ = None
    placeholder = '%s'

    def connect(self, **kwargs):
        '''
        mincached : 启动时开启的空连接数量(缺省值 0 意味着开始时不创建连接)
        maxcached: 连接池使用的最多连接数量(缺省值 0 代表不限制连接池大小)
        maxshared: 最大允许的共享连接数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量，被请求为共享的连接将会被共享使用。
        maxconnections: 最大允许连接数量(缺省值 0 代表不限制)
        blocking: 设置在达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误；其他代表阻塞直到连接数减少)
        maxusage: 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用)。当达到最大数值时，连接会自动重新连接(关闭和重新打开)
        '''
        db_host = kwargs.get('db_host', 'localhost')
        db_port = kwargs.get('db_port', 3306)
        db_user = kwargs.get('db_user', 'root')
        db_pwd = kwargs.get('db_pwd', '')
        db = kwargs.get('db', '')

        self.pool = PooledDB(pymysql, mincached=20, maxcached=50, maxconnections=200, host=db_host,
            user=db_user, passwd=db_pwd, db=db, port=db_port, charset='utf8')

        logger.info('''connect mysql db_host:%s db_port:%d db_user:%s 
            db_pwd:%s db:%s''', db_host, db_port, db_user, db_pwd, db)

    @staticmethod
    def escape(string):
        pass

    def _check_parameter(self, sql_query, values):
        count = sql_query.count('%s')
        if count > 0:
            for elem in values:
                if not elem:
                    logger.debug('sql_query:%s values:%s check failed',
                        sql_query, values)
                    return False
        return True

    def get_conn(self):
        '''
        返回一个连接池中的链接
        '''
        conn = self.pool.connection()
        return conn

    def _execute(self, sql_query, values=[]):
        '''
        每次都使用新的连接池中的链接
        '''
        if not self._check_parameter(sql_query, values): 
            return
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_query, values)
        conn.commit()
        r = cur.fetchall()
        logger.debug('execute sql_query:%s', sql_query)
        return r, conn

    def _execute_bulk(self, sql_query, bulkdata=[]):    #批量插入数据
        '''
        每次都使用新的连接池中的链接
        '''
        conn = self.pool.connection()
        try:
            cur = conn.cursor()
            cur.executemany(sql_query, bulkdata)
            conn.commit()
            logger.info('_execute_bulk sql_query:%s', sql_query)
        except:
            conn.rollback()
            logger.error('exception when execute sql_query: %s, exception: %s', sql_query, traceback.format_exc())
        return conn

    def insert(self,sql_insert,bulkdata=[]):
        conn = self.pool.connection()
        try:
            cur = conn.cursor()
            cur.executemany(sql_insert, bulkdata)
            conn.commit()
            logger.info('_execute_bulk sql_insert:%s', sql_insert)
        except:
            conn.rollback()
            logger.error('exception when execute sql_insert: %s, exception: %s', sql_insert, traceback.format_exc())
        return conn

    def select(self, sql_query, values=[]):
        if not self._check_parameter(sql_query, values):
            return
        r, conn = self._execute(sql_query, values)
        for row in r:
            yield row
        conn.close()

    def execute(self, sql_query, values=[]):
        cur, conn = self._execute(sql_query, values)
        conn.close()

    def insert_bulkdata(self, bulkdata, table):   #bulkdata为列表，元素是字典
        if len(bulkdata) == 0:
            return
        key_list = []
        values_list = []
        for key in bulkdata[0].keys():
            key_list.append(key)
        for value_dict in bulkdata:
            item_list = []
            for key in key_list:
                item_list.append(value_dict[key])
            values_list.append(tuple(item_list))
        keys_str = ','.join(key_list)
        values_str = ','.join(['%s'] * len(key_list))
        sql_query = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys_str, values=values_str)

        conn = self._execute_bulk(sql_query, tuple(values_list))
        conn.close()

    def insert_dict(self, table, data={}):
        '''
        插入一条数据
        :param table:
        :param data: {}
        :return:
        '''
        conn = self.pool.connection()
        try:
            cur = conn.cursor()
            sql_insert = "insert into {} ({}) values {}".format(table, ','.join(list(data.keys())),
                                                                tuple(data.values()))
            logger.debug(sql_insert)
            cur.execute(sql_insert)
            conn.commit()
        except Exception:
            conn.rollback()
            logger.error('exception when execute insert sql_insert '
                         'exception: %s', traceback.format_exc())


