import os
import pandas as pd
import requests
import json
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts import options
from pyecharts.globals import GeoType

info_table = pd.DataFrame(columns=['位置', '次数'])
row = 0

ddata = {}

def formatdata(filenames):
    global row
    for filename in filenames:
        f = open(os.path.join('./爬取结果/', filename), encoding='gb18030')
        data = pd.read_csv(f, encoding='gb18030', header=None)
        data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签']
        for i in range(0, len(data)):
            if data['小区名'].iloc[i] not in ddata:
                ddata[data['小区名'].iloc[i]] = 1
            else:
                ddata[data['小区名'].iloc[i]] += 1
        print(filename, 'finished')

    for i in range(0, len(list(ddata.values()))):
        alist = []
        alist.append(list(ddata.keys())[i])
        alist.append(list(ddata.values())[i])
        info_table.loc[row] = alist
        row += 1
    info_table.to_csv('./临时数据文件/频数统计.csv', encoding='gb18030')
    print('频数统计完成！')

def gain_location(address):
    #这个api_url网址里的city=填你想填的城市名（非必需参数，即可删除city=xxx），ak=填入你自己的密匙，output=json意思是输出json格式
    api_url = f'http://api.map.baidu.com/geocoding/v3/?city=北京市&address={address}&ak=cU38ZCTGT8Psgkcmlh2bD8THnKP2kH3H&output=json&callback=showLocation'

    r = requests.get(api_url)
    r = r.text

    '''经历以下两次去除，使得最终结果为json格式的数据 
       原来的数据格式：showLocation&&showLocation(' showLocation&&showLocation('showLocation&&showLocation({"status":0,"result":{"location":{"lng":108.94646555063274,"lat":34.34726881662395},"precise":0,"confidence":12,"comprehension":63,"level":"城市"}}）
       去除后的数据格式为将json字符串转换为字典类型：showLocation&&showLocation({"status":0,"result":{"location":{"lng":108.94646555063274,"lat":34.34726881662395},"precise":0,"confidence":12,"comprehension":63,"level":"城市"}}
    '''
    r = r.strip('showLocation&&showLocation(')
    r = r.strip(')')

    jsonData = json.loads(r)  # 将json字符串转换为字典类型转为字典格式类型

    return jsonData

def Bmap(filename):
    g = Geo(init_opts=opts.InitOpts(
        width='1800px',
        height='900px',
    )).add_schema(maptype="广州")

    stationid_list = []
    Longitude_list = []
    Latitude_list = []
    point_list = []
    file = pd.read_csv(filename, encoding='gb18030')
    for i in range(0, len(file)):
        stationid_list.append(file['地点'].iloc[i])
        Longitude_list.append(file['经度'].iloc[i])
        Latitude_list.append(file['纬度'].iloc[i])
        point_list.append(file['频数'].iloc[i])

    # 给所有点附上标签 'StationID'
    for i in range(0, len(stationid_list)):
        g.add_coordinate(stationid_list[i], Longitude_list[i], Latitude_list[i])

    # 给每个点赋值
    # for i in range(0, len(stationid_list)):
    for i in range(0, len(file)):
        data_pair = []
        data_pair.append((stationid_list[i], int(point_list[i])))
        if int(point_list[i]) <= 3:
            g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=3)
        else:
            g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=int(point_list[i]))

    # 画图
    # g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=8)
    g.set_series_opts(label_opts=options.LabelOpts(is_show=False))
    g.set_global_opts(title_opts=options.TitleOpts(title="全地点热力图展示"))

    # 保存结果到 html
    result = g.render('./分析图表/二手房频数地理热力图.html')
    print('地理热力图生成完毕！')

def lalo_change(data):
    row1 = 0
    for i in range(0, len(data)):
        address = data['位置'].iloc[i]
        location = gain_location(address)
        lng = location['result']['location']['lng']
        lat = location['result']['location']['lat']

        alist = []
        alist.append(data['位置'].iloc[i])
        alist.append(data['次数'].iloc[i])
        alist.append(lng)
        alist.append(lat)
        info_table2.loc[row1] = alist
        row1 += 1

    info_table2.to_csv('./临时数据文件/经纬度转换.csv', encoding='gb18030')
    print('经纬度转换完毕！')

if __name__ == '__main__':
    f = []
    filenames = os.listdir('./爬取结果/')  # 设定调用文件的相对路径
    for i in filenames:
        if '.csv' in str(i):
            f.append(i)
    filenames = f
    formatdata(filenames)

    info_table2 = pd.DataFrame(columns=['地点', '频数', '经度', '纬度'])

    data = pd.read_csv('./临时数据文件/频数统计.csv', encoding='gb18030')
    lalo_change(data)

    Bmap('./临时数据文件/经纬度转换.csv')