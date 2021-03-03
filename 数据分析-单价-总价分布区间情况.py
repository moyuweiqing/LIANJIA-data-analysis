import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Pie

def draw_pie(xlist, ylist, xlist2, ylist2, name):
    data_pair = [list(z) for z in zip(xlist, ylist)]
    data_pair2 = [list(z) for z in zip(xlist2, ylist2)]
    c = (
        Pie(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
        .set_global_opts(title_opts=opts.TitleOpts(
            title=name
            ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .add(
            '广州二手房单价分布图',
            data_pair=data_pair,
            center=["20%", "40%"],
            radius=[60, 90],
        )
        .add(
            '广州二手房总价分布图',
            data_pair=data_pair2,
            center=["60%", "40%"],
            radius=[60, 90],
        )
        .render('./分析图表/' + name + '.html')
    )

def calulate(filenames):
    ydic = {'20000元以下': 0, '20000-30000元': 0, '30000-40000元': 0, '40000-50000元': 0, '50000-60000元': 0, '60000-70000元': 0,'70000-80000元': 0, '80000-90000元': 0, '90000-100000元': 0, '100000元以上': 0}
    ydic2 = {'100万以下': 0, '100-200万': 0, '200-300万': 0, '300-400万': 0, '400-500万': 0, '500-600万': 0, '600-700万': 0, '700-800万': 0, '800-900万': 0, '900-1000万': 0, '1000万以上': 0}
    for filename in filenames:
        data = pd.read_csv(os.path.join('./爬取结果', filename), encoding='gb18030', header=None)
        data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签']
        for i in data['单价']:
            price = int(i)
            if price <= 20000:
                ydic['20000元以下'] += 1
            elif price > 20000 and price <= 30000:
                ydic['20000-30000元'] += 1
            elif price > 30000 and price <= 40000:
                ydic['30000-40000元'] += 1
            elif price > 40000 and price <= 50000:
                ydic['40000-50000元'] += 1
            elif price > 50000 and price <= 60000:
                ydic['50000-60000元'] += 1
            elif price > 60000 and price <= 70000:
                ydic['60000-70000元'] += 1
            elif price > 70000 and price <= 80000:
                ydic['70000-80000元'] += 1
            elif price > 80000 and price <= 90000:
                ydic['80000-90000元'] += 1
            elif price > 90000 and price <= 100000:
                ydic['90000-100000元'] += 1
            elif price > 100000:
                ydic['100000元以上'] += 1

        for i in data['总价']:
            price = int(i)
            if price <= 1000000:
                ydic2['100万以下'] += 1
            elif price > 1000000 and price <= 2000000:
                ydic2['100-200万'] += 1
            elif price > 2000000 and price <= 3000000:
                ydic2['200-300万'] += 1
            elif price > 3000000 and price <= 4000000:
                ydic2['300-400万'] += 1
            elif price > 4000000 and price <= 5000000:
                ydic2['400-500万'] += 1
            elif price > 5000000 and price <= 6000000:
                ydic2['500-600万'] += 1
            elif price > 6000000 and price <= 7000000:
                ydic2['600-700万'] += 1
            elif price > 7000000 and price <= 8000000:
                ydic2['700-800万'] += 1
            elif price > 8000000 and price <= 9000000:
                ydic2['800-900万'] += 1
            elif price > 9000000 and price <= 10000000:
                ydic2['900-1000万'] += 1
            elif price > 100000:
                ydic2['1000万以上'] += 1
    draw_pie(list(ydic.keys()), list(ydic.values()), list(ydic2.keys()), list(ydic2.values()), '广州二手房单价-总计分布图')

if __name__ == '__main__':
    filenames = os.listdir('./爬取结果')
    calulate(filenames)