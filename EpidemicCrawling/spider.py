# -*- Coding:UTF-8 -*-
# @Time    : 2022/06/21 0:17
# @Author  : Beluga
# @Version : Python 3.10.4
#  爬取中国疫情数据
import datetime

import requests
import pandas as pd
from sqlalchemy import create_engine


# 爬取疫情数据
def crawl_china_data():
    # 爬取网址
    url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list"
    # 请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.41',
        'host': "api.inews.qq.com"
    }
    # 请求参数
    parameters = {
        'modules': 'chinaDayList,chinaDayAddList,provinceCompare'
    }
    # 获取响应,成功响应为 200 状态码,加入请求头是为了模拟浏览器获取数据
    response = requests.get(url=url, headers=headers, params=parameters)
    # 获取所有的疫情数据
    all_data = response.json()["data"]

    # 每个省份的总数据（每日更新）
    provinceCompare = all_data["provinceCompare"]
    # 最近一个月的全国疫情的总数据
    chinaDayList = all_data["chinaDayList"]
    # 最近一个月的全国疫情的新增数据
    chinaDayAddList = all_data["chinaDayAddList"]

    return provinceCompare, chinaDayList, chinaDayAddList


# 解析数据
def parse_china_data(day_list, day_add_list):
    # 解析每日累计数据、每日新增
    day_df = pd.DataFrame(day_list)
    day_add_df = pd.DataFrame(day_add_list)
    # 格式化日期 "data": "2022-6-21"
    day_df["date"] = pd.to_datetime(day_df["y"] + "." + day_df["date"], format="%Y-%m-%d")
    day_add_df["date"] = pd.to_datetime(day_add_df["y"] + "." + day_add_df["date"], format="%Y-%m-%d")
    # 保存数据
    save_china_data(day_df, "day_list", "replace")
    save_china_data(day_add_df, "day_add_list", "replace")


def pares_province_data(province_list):
    date = []  # 日期
    province = []  # 省份
    nowConfirm = []  # 现在确诊
    confirmAdd = []  # 新增确诊
    dead = []  # 死亡
    heal = []  # 治愈
    zero = []  # 无症状

    for province_name, province_info in province_list.items():
        province.append(province_name)
        date.append(datetime.datetime.now().strftime("%Y-%m-%d"))
        nowConfirm.append(province_info.get("nowConfirm", 0))
        confirmAdd.append(province_info.get("confirmAdd", 0))
        dead.append(province_info.get("dead", 0))
        heal.append(province_info.get("heal", 0))
        zero.append(province_info.get("zero", 0))

    df = pd.DataFrame({
        "province": province,
        "date": date,
        "nowConfirm": nowConfirm,
        "confirmAdd": confirmAdd,
        "dead": dead,
        "heal": heal,
        "zero": zero
    })
    save_china_data(df, 'province_list', "replace")


# 保存数据
def save_china_data(df, table_name, if_exists="replace"):
    # 获取数据库连接
    conn = create_engine('mysql://root:root@localhost:3306/epidemic?charset=utf8')
    # 利用pd的io中的sql的to_sql方法进行导入，参数为(数据, '表名', con=连接键, schema='数据库名', if_exists='操作方式')
    pd.io.sql.to_sql(df, table_name, con=conn, if_exists=if_exists, index=None)


if __name__ == '__main__':
    provinceCompare, chinaDayList, chinaDayAddList = crawl_china_data()
    parse_china_data(chinaDayList, chinaDayAddList)
    pares_province_data(provinceCompare)
    print("爬取数据完成")
