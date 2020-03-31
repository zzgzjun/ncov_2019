import json
import string
import time
from datetime import datetime
from jieba.analyse import extract_tags
import requests


# def catch_distribution():
#     url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
# # requests.get(url)
#     data={}
#     for item in json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children']:
#         if item['name'] not in data:
#             data.update({item['name']:0})
#         for city_data in item['children']:
#             data[item['name']] += int(city_data['total']['confirm'])
#     return data
from myapp.models import HotSearch


def catch_hotsearch():
    from selenium.webdriver import Chrome, ChromeOptions
    import time
    url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
    broswer = Chrome()
    broswer.get(url)
    tag = broswer.find_element_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/div')
    tag.click()
    time.sleep(1)
    content=[]
    c = broswer.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    for i in c:
        content.append(i.text)
    broswer.close()
    return content


def hotsearch_dis():
    data=catch_hotsearch()
    result=[]
    for row in data:
        k=row.rstrip(string.digits) #移除热搜数字
        v=row[len(k):]
        ks=extract_tags(k)
        for j in ks:
            if not j.isdigit():
                result.append({'name':j,"value":v})
    return result


def insert_hotsearch():
    data=hotsearch_dis()
    for i in data:
        hot=HotSearch()
        hot.date=datetime.now()
        hot.name=i['name']
        hot.value=i['value']
        hot.save()
    return '插入数据成功'


def catch_city():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    data_all=json.loads(requests.get(url=url).json()['data'])
#     data = json.loads(requests.get(url=url).json()['data'])['areaTree'][0]['children']
    data = data_all['areaTree'][0]['children']
    date=data_all['lastUpdateTime']
    city_data=[]
    for item in data:
        province = item['name']
        for i in item['children']:
            city = i['name']
            nowConfirm = i['total']['nowConfirm']
            confirm = i['total']['confirm']
            suspect = i['total']['suspect']
            dead = i['total']['dead']
            heal = i['total']['heal']
            d = [date,province, city, nowConfirm, confirm, suspect, dead, heal]
            city_data.append(d)
    return city_data


def catch_daily():
    """抓取每日确诊和死亡数据"""
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts&callback=&_=%d' % int(time.time() * 1000)
    data = json.loads(requests.get(url=url).json()['data'])
    data.sort(key=lambda x: x['date'])
    date_list = list()  # 日期
    confirm_list = list()  # 确诊
    confirm_add_list = list()  # 确诊
    suspect_list = list()  # 疑似
    suspect_add_list = list()  # 疑似
    dead_list = list()  # 死亡
    dead_add_list = list()  # 死亡
    heal_list = list()  # 治愈
    heal_add_list = list()  # 治愈
    for item in data:
        month, day = item['date'].split('/')
        date_list.append(datetime.strptime('2020-%s-%s' % (month, day), '%Y-%m-%d'))
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))

    for i in range(len(confirm_list) - 1):
        b = confirm_list[i + 1] - confirm_list[i]  # 后者减前者
        confirm_add_list.append(b)  # 添加元素到新列表
    confirm_add_list.insert(0, confirm_list[0])

    for i in range(len(suspect_list) - 1):
        b = suspect_list[i + 1] - suspect_list[i]  # 后者减前者
        suspect_add_list.append(b)  # 添加元素到新列表
    suspect_add_list.insert(0, suspect_list[0])

    for i in range(len(dead_list) - 1):
        b = dead_list[i + 1] - dead_list[i]  # 后者减前者
        dead_add_list.append(b)  # 添加元素到新列表
    dead_add_list.insert(0, dead_list[0])

    for i in range(len(heal_list) - 1):
        b = heal_list[i + 1] - heal_list[i]  # 后者减前者
        heal_add_list.append(b)  # 添加元素到新列表
    heal_add_list.insert(0, heal_list[0])
    return date_list, confirm_list,confirm_add_list, suspect_list,suspect_add_list, dead_list,dead_add_list, heal_list,heal_add_list


if __name__== '__main__':
    # content=catch_hotsearch()
    # print(content)
    # data=hotsearch_dis()
    # print(data)
    insert_hotsearch()