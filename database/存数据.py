import requests
import json
import pymysql
import time

# 存数据库
def insert_into_postgres(table: str, fields: str, values: list) -> None:
    '''
    :param table: 表名
    :param fields:  字段名
    :param values:  数据列表，每一项是一条记录的列表
    :return: None
    '''
    couunt = len(str(fields).split(','))
    fields = ",".join(str(fields).split(','))
    placeholder = ",".join(['%s'] * couunt)
    conn = psycopg2.connect(database="test", user="postgres", password="123456",
                            host="localhost", port="5432")
    cursor = conn.cursor()
    sql = "insert into " + table + "(" + fields + ")" + " values(" + placeholder + ")"
    cursor.executemany(sql, values)
    conn.commit()
    conn.close()

# 修改表注释
def create_table_comment():
    # 格式： 列1（字段名）   列二（注释）
    # 读取数据
    data = pd.read_excel(r'已解密.xlsx', header=0,sheet_name="数据字典")
    conn = psycopg2.connect(database="test", user="postgres", password="123456",
                            host="localhost", port="5432")
    cursor = conn.cursor()
    table_name = "sample"  # 表名
    for idx, row in data.iterrows():
        row = list(row)
        field = row[0]
        comment = row[1]
        sql = f"""COMMENT  ON COLUMN  {table_name}.{field} IS '{comment}'"""
        cursor.execute(sql)
        conn.commit()
    conn.close()

if __name__ == '__main__':
    pass




