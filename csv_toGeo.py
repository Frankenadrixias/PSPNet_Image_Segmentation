import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# 将csv文件转储为shape文件
def csv_to_points(input_path):

    # 读取文件，编码方式为utf-8
    df = pd.read_csv(input_path, header=0, encoding='utf-8')

    # 根据对应的经纬度字段定位坐标点
    geo_point = [Point(xy) for xy in zip(df.lng, df.lat)]

    # 指定WGS84坐标系
    geoDataFrame = gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=geo_point)

    print(input_path + '---finished')

    return geoDataFrame
