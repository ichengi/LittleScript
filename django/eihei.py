#django 反向icontains
# r_city_zh 是变量  n_city_zh是数据库字段
with connection.cursor() as cursor:
  cursor.execute(f" select * from {t_table_name} where '{r_city_zh}' like concat('%',n_city_zh,'%'")
  temp_row = cursor.fetchonr()
  temp_city_code = row[0]
  
