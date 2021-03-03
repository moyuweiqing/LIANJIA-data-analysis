import pandas as pd
import re
from lxml import etree

def getIntoPage(region, text):
    info_table = pd.DataFrame(
        columns=['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签'])
    row_num = 0

    # 框架转换
    html_text = etree.HTML(text)

    for i in range(1, 31):
        name_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[1]/a/text()'
        position_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[2]/div/a[1]/text()'
        position_url2 = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[2]/div/a[2]/text()'
        labels_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[3]/div/text()'
        followers_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[4]/text()'
        total_price_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[6]/div[1]/span[1]/text()'
        price_url = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[6]/div[2]/span/text()'

        name = html_text.xpath(name_url)
        position = html_text.xpath(position_url)
        position2 = html_text.xpath(position_url2)
        labels = html_text.xpath(labels_url)
        followers = html_text.xpath(followers_url)
        total_price = html_text.xpath(total_price_url)
        price = html_text.xpath(price_url)

        alist = []
        # alist.append(region)
        alist.append(name[0])
        alist.append(position[0].replace(' ', ''))
        alist.append(position2[0].replace(' ', ''))

        labels = labels[0].split('|')
        if len(labels) < 7:
            continue
        else:
            for label in labels:
                # 数据处理
                if '平米' in label:
                    label = str(float(label.replace('平米', '')))
                if '层' in label:
                    label = re.findall("\d+",label)[0]
                if '年建' in label:
                    label = label.replace(' ', '').replace('年建', '')

                alist.append(label)

        followers = followers[0].split('/')
        if len(followers) < 2:
            continue
        else:
            for follower in followers:
                if '人关注' in follower:
                    follower = follower.replace(' ', '').replace('人关注', '')
                if '天以前发布' in follower:
                    follower = follower.replace(' ', '').replace('天以前发布', '')
                alist.append(follower)

        alist.append(float(total_price[0]) * 10000)
        alist.append(price[0].replace('单价', '').replace('元/平米', ''))

        blist = ''
        for j in range(1, 6):
            try:
                xpath = '//*[@id="content"]/div[1]/ul/li[' + str(i) + ']/div[1]/div[5]/span[' + str(j) + ']/text()'
                t = html_text.xpath(xpath)
                blist += t[0]
                blist += ' '
            except:
                break
        alist.append(blist)

        if len(alist) == 15:
            info_table.loc[row_num] = alist
            row_num += 1
        else:
            continue
    return info_table