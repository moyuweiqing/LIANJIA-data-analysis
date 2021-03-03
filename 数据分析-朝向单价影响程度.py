import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Pie

regions_dic = {'tianhe': '天河', 'yuexiu': '越秀', 'liwan': '荔湾', 'haizhu': '海珠', 'panyu': '番禺', 'baiyun': '白云',
               'huangpugz': '黄埔', 'conghua': '从化', 'zengcheng': '增城', 'huadou': '花都', 'nansha': '南沙'}

def draw(data):
    c = (
        Pie(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
            .add(
            "",
            [list(z) for z in zip(data.keys(), data.values())]
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="广州二手房各房型受关注情况图"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render('分析图表/' + "广州二手房各房型受关注情况图.html")
    )

def read_csv():
    file = 'tianhe.csv'
    data = pd.read_csv('./爬取结果/' + file, encoding='gb18030', header=None)
    data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签']
    data['是否东南朝向'] = ''
    for i in range(0, len(data)):
        if '南' in data['朝向'].iloc[i].split(' ') or '东' in data['朝向'].iloc[i].split(' ') or '东南' in data['朝向'].iloc[i].split(' '):
            data['是否东南朝向'].iloc[i] = '是'
        else:
            data['是否东南朝向'].iloc[i] = '否'
    print(data.head())
    a = data['单价'].groupby([data['小区名'], data['是否东南朝向']]).mean()
    a.to_csv('test.csv', encoding='gb18030')

if __name__ == '__main__':
    read_csv()