def latitude_and_longitude_convert_to_decimal_system(*arg):
    """
    经纬度转为小数
    :param arg:
    :return: 十进制小数
    """
    return float(arg[0]) + ((float(arg[1]) + (float(arg[2].split('/')[0]) / float(arg[2].split('/')[-1]) / 60)) / 60)


# 获取照片中的经纬度信息
def get_pos1(jppgpath: str):
    # res :{'LatitudeRef': 'N', 'Latitude': 30.47733852777778, 'LongitudeRef': 'E', 'GPSLongitude': 104.01457041666667,
    #  'AltitudeRef': '0', 'GPSAltitude': 513.976}
    GPS = {}
    GPS['Path'] = jppgpath
    f = open(jppgpath, 'rb')
    tags = exifread.process_file(f)
    for tag, value in tags.items():
        if re.match('GPS GPSLatitudeRef', tag):
            GPS['LatitudeRef'] = str(value)
        elif re.match('GPS GPSLongitudeRef', tag):
            GPS['LongitudeRef'] = str(value)
        elif re.match('GPS GPSAltitudeRef', tag):
            GPS['AltitudeRef'] = str(value)
        elif re.match('GPS GPSLatitude', tag):
            try:
                match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                GPS['Y'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
            except:
                deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                GPS['Y'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
        elif re.match('GPS GPSLongitude', tag):
            try:
                match_result = re.match('\[(\w*),(\w*),(\w.*)/(\w.*)\]', str(value)).groups()
                GPS['X'] = int(match_result[0]), int(match_result[1]), int(match_result[2])
            except:
                deg, min, sec = [x.replace(' ', '') for x in str(value)[1:-1].split(',')]
                GPS['X'] = latitude_and_longitude_convert_to_decimal_system(deg, min, sec)
        elif re.match('GPS GPSAltitude', tag):
            GPS['Altitude'] = eval(str(value))
        elif re.match('.*Date.*', tag):
            date = str(value)
    # GPS.pop('LatitudeRef')
    # GPS.pop('LongitudeRef')
    # GPS.pop('AltitudeRef')
    return GPS
  
  
# 将数据写入excel
def write2excel(resexcelfile:str，posdata:'pandas.core.frame.DataFrame'):
    sheetname = 'sheet1'
        
    writer = pd.ExcelWriter(resexcelfile, engine='openpyxl')
    for idx, row in posdata.iterrows():
        posdata.loc[idx, 'Path'] = os.path.join(dirpath, posdata.loc[idx, 'Path'])
    posdata.to_excel(excel_writer=writer, sheet_name=sheetname, index=False)  # 数据页

    writer.save()
    writer.close()
  
  
  
