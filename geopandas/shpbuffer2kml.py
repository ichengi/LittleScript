def buffer(inShp:str, fname:str, bdistance=0.0005:float)-> Bool:
    """
    :param inShp: 输入的矢量路径
    :param fname: 输出的矢量路径
    :param bdistance: 缓冲区距离
    : return:
    """
    ogr.UseExceptions()
    in_ds = ogr.Open(inShp)
    in_lyr = in_ds.GetLayer()
    # 创建输出Buffer文件
    driver = ogr.GetDriverByName('kml')
    if Path(fname).exists():
        out_ds=driver.Open(fname)
    else:
        # 新建DataSource，Layer
        out_ds = driver.CreateDataSource(fname)
        # driver.DeleteDataSource(fname)
    out_lyr = out_ds.CreateLayer(fname, in_lyr.GetSpatialRef(), ogr.wkbPolygon)
    def_feature = out_lyr.GetLayerDefn()
    # 遍历原始的Shapefile文件给每个Geometry做Buffer操作
    for feature in in_lyr:
        geometry = feature.GetGeometryRef()
        buffer = geometry.Buffer(bdistance,quadsecs=2)  # quadsecs: the number of segments used to approximate a 90 degree

        # buffer = geometry.GetGeometryRef().Buffer(0)
        out_feature = ogr.Feature(def_feature)
        out_feature.SetGeometry(buffer)
        out_lyr.CreateFeature(out_feature)
        # print(out_lyr.GetExtent())
        out_feature = None
    out_ds.FlushCache()
    del in_ds, out_ds
    return 1
