# -*-coding:utf-8-*-
'''
csv文件结构： [['lon','lat'],[104,30],[104,30].......] 可以添加相应的字段，默认设置成字符串
'''
import os

import geopandas
import pyproj
import pandas as pd

def csv2shp(csv_path: str, shp_path: str, crs: str) -> None:
    df = geopandas.read_file(csv_path, encoding='utf-8')
    df[['lon', 'lat']] = df[['lon', 'lat']].apply(pd.to_numeric)
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lon, df.lat))
    gdf.crs = pyproj.CRS.from_user_input(crs)  # 给输出的shp增加投影
    # gdf.rename(columns={'name':'ave_price'},inplace=True)  # 可以改名字
    gdf.to_file(shp_path, driver='ESRI Shapefile', encoding='utf-8')


if __name__ == '__main__':
    csv_path = r"F:\csvdata"  # csv文件所在目录
    shp_path = r"F:\resdata"  # 生成结果目录
    crs = 'EPSG:4326'  # 坐标系
    for item in os.listdir(csv_path):
        if item.endswith('.csv'):
            print(item)
            csv2shp(os.path.join(csv_path, item), os.path.join(shp_path, (item.split('.')[0] + '.shp')), crs)
