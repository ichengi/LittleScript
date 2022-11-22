# -*-coding:utf-8-*-
import math
import os.path

import pandas as pd

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方

def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]

def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]

def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]

def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)

def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)

def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

# 转换坐标
def translate():
    print("开始转换数据")
    if file_path.endswith('csv'):
        translate_csv(file_path)
    elif file_path.endswith('xls') or file_path.endswith('xlsx'):
        translate_excel(file_path)
    else:
        print(f'不支持的文件格式！{file_path} 转换失败')
    print("转换完成！")
        

#转换csv中的坐标
def translate_csv(file_path):
    data = pd.read_csv(file_path, encoding="utf-8")
    for idx, row in data.iterrows():
        temp_res = eval(f"{trans_method}(float(data.loc[idx, lon_field_name]), float(data.loc[idx, lat_field_name]))")
        data.loc[idx, lon_field_name] = temp_res[0]
        data.loc[idx, lat_field_name] = temp_res[1]
    save_data(data,'sheet1') # 这里如果保存为excel 默认给一个sheet名字

#转换excel中的坐标
def translate_excel(file_path):
    df = pd.read_excel(file_path,sheet_name=None)
    writer = pd.ExcelWriter(save_file_path)
    for sheet_name in df:
            print(f"开始处理sheet {sheet_name}")
            data = pd.read_excel(file_path, sheet_name=sheet_name)
            try:
                for idx, row in data.iterrows():
                    temp_res = eval(f"{trans_method}(float(data.loc[idx, lon_field_name]), float(data.loc[idx, lat_field_name]))")
                    data.loc[idx, lon_field_name] = temp_res[0]
                    data.loc[idx, lat_field_name] = temp_res[1]
            except:
                print(f'错误！ "{sheet_name}"可能不包含{lon_field_name}，{lat_field_name} 这两个字段 跳过')
            data.to_excel(writer,index=False,sheet_name=sheet_name)
    writer.save()

# 保存数据
def save_data(data,sheet_name):
    if save_file_path.endswith('csv'):
        save_as_csv(data)
    elif save_file_path.endswith('xls') or save_file_path.endswith('xlsx'):
        save_as_excel(data,sheet_name)
    else:
        print(f'不支持的文件格式！{save_file_path} 存储失败')

# 保存为csv
def save_as_csv(data):
    data.to_csv(save_file_path,index=False)

# 保存为excel
def save_as_excel(data,sheet_name):
    data.to_excel(save_file_path,index=False, sheet_name=sheet_name)

if __name__ == '__main__':
    # 文件类型只支持xls  xlsx  csv
    file_path = r"1.xls" # 源文件路径
    save_file_path = r"2.xlsx" # 保存文件路径
    lon_field_name = "经度" # 经度字段对应的字段名
    lat_field_name = "纬度" # 纬度字段对应的字段名
    trans_method = "bd09_to_wgs84" # 坐标转换方法

    # 高德转百度：gcj02_to_bd09
    # 百度转高德：bd09_to_gcj02
    # wgs84转高德：wgs84_to_gcj02
    # 高德转wgs84：gcj02_to_wgs84
    # 百度转wgs84：bd09_to_wgs84
    # wgs84转百度：wgs84_to_bd09
    translate()

