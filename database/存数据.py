import requests
import json
import pymysql
import time

if __name__ == '__main__':
    # 连接数据库
    conn = pymysql.connect(host='localhost', user="root", password="123456" , database="test", charset="utf8")
    cursor = conn.cursor()

    # 插入sql语句
    sql = "insert into table123 (deviceName,value123,times) values (%s,%s,%s)"
    lists = []
    for list in lists:
        deviceName = str(list[0])
        value = str(list[1])
        times = list[2]

        # 执行插入操作
        insert = cursor.execute(sql, (deviceName, value, times))

    rs = cursor.fetchall()
    for r in rs:
        print(r)


    cursor.close()
    conn.commit()
    conn.close()




