import pandas as pd
import os
from wordcloud import WordCloud

def draw_wordcloud(filenames):
    # 租房标签词云图
    labels_dic = {}
    for filename in filenames:
        data = pd.read_csv(os.path.join('./爬取结果', filename), encoding='gb18030', header=None)
        data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签']
        for i in data['标签']:
            try:
                elements = i.split(' ')
                for element in elements:
                    if element != '':
                        if element in labels_dic:
                            labels_dic[element] += 1
                        else:
                            labels_dic[element] = 1
            except:
                continue
    wc = WordCloud(font_path='simkai.ttf', max_words=100, width=1920, height=1080, margin=5)
    wc.generate_from_frequencies(labels_dic)
    wc.to_file('./分析图表/广州二手房标签词云图.png')

if __name__ == '__main__':
    filenames = os.listdir('./爬取结果')
    draw_wordcloud(filenames)