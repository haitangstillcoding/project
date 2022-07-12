# -*- Coding:UTF-8 -*-
# @Time    : 2022/06/21 0:20
# @Author  : Beluga
# @Version : Python 3.10.4
# @Desc    : 工具类
import traceback
import pandas as pd
from sqlalchemy import create_engine


class utils:
    # 构造方法,初始化参数为数据库名、数据库账号、数据库密码、数据库表名
    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password

    # 根据sql语句查询数据库疫情信息
    def query(self, table_name, use_sql=None):
        try:
            # 获取mysql数据库连接
            conn = create_engine(
                'mysql://{}:{}@localhost:3306/{}?charset=utf8'.format(self.user, self.password, self.db_name))
            # 简写 if else, use_sql有参数则使用参数sql，没有参数则查询所有表中所有字段
            sql = use_sql if use_sql else "select * from {}".format(table_name)
            # 使用pandas的read_sql函数,从mysql数据库中读取疫情数据
            epidemic = pd.read_sql(sql, con=conn)
            return epidemic
        except Exception as e:
            # 异常处理
            traceback.print_exc(e)
            return None

    # 获取c1的四个数据：累计确诊、累计治愈、累计死亡、现存确诊
    def get_c1_data(self):
        sql = "select date, confirm, heal,dead,nowConfirm from day_list order by date desc limit 1"
        df = self.query("day_list", sql)
        confirm = int(df["confirm"][0])
        heal = int(df["heal"][0])
        dead = int(df["dead"][0])
        now_confirm = int(df["nowConfirm"][0])
        return [confirm, heal, dead, now_confirm]

    # 获取中国各省的新增疫情数据
    def get_c2_data(self):
        dict_data = {}
        sql = "select distinct date,province,zero from province_list order by date desc limit 34"
        df = self.query("province_list", sql)
        for p, v in zip(df.province, df.zero):
            dict_data[p] = v
        return dict_data

    # 获取疫情期间每日累计数据
    def get_l1_data(self):
        sql = "select date, importedCase, noInfect, dead from day_list order by date asc"
        df = self.query("day_list", sql)
        return df

    # 获取疫情期间每日新增数据
    def get_l2_data(self):

        sql = "select date, localConfirmadd,heal,dead from day_add_list order by date asc"
        df = self.query("day_add_list", sql)
        return df

    # 获取前五名省份无症状感染者数据
    def get_r1_data(self):
        sql = "select province,zero from province_list order by zero desc limit 10"
        df = self.query("province_list", sql)
        return df

    # 获取全国累计
    def get_r2_data(self):
        sql = "select date,heal,nowConfirm,confirm from day_list order by date desc limit 1"
        df = self.query("day_list", sql)
        return df
