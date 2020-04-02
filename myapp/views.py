from  datetime import datetime
import json

from django.core import serializers
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

from myapp.models import History, Detail, HotSearch
from utils import spider
# Create your views here.
from utils.spider import hotsearch_dis
from utils.utils import get_time


def add(request):
    date, confirm,confirm_add, suspect,suspect_add, dead,dead_add, heal,heal_add=spider.catch_daily()
    for i in range(len(date)):
        data_info=History()
        data_info.date=date[i]
        data_info.confirm=confirm[i]
        data_info.confirm_add=confirm_add[i]
        data_info.suspect=suspect[i]
        data_info.suspect_add=suspect_add[i]
        data_info.dead=dead[i]
        data_info.dead_add=dead_add[i]
        data_info.heal=heal[i]
        data_info.heal_add=heal_add[i]
        data_info.save()
    # print(confirm,confirm_add,suspect)
    return HttpResponse('数据插入成功')


def insert_hotsearch(request):
    data=hotsearch_dis()
    for i in data:
        hot=HotSearch()
        hot.date=datetime.now()
        hot.name=i['name']
        hot.value=i['value']
        hot.save()
    return HttpResponse('数据插入成功')

def index(request):
    history_list = History.objects.values_list('confirm_add','confirm','suspect','dead','heal')
    history_list = list(history_list)

    data=[
        ['date', '确诊', '疑似', '死亡', '治愈'],
        ['01.13', 1001, 0, 1, 0],
        ['01.14', 41, 0, 1, 0],
        ['01.15', 41, 0, 2, 5],
        ['01.16', 45, 0, 2, 8],
        ['01.17', 62, 0, 2, 12],
        ['01.18', 198, 0, 3, 17],
        ['01.19', 275, 0, 4, 18],
        ['01.20', 291, 54, 6, 25],
        ['01.21', 440, 37, 9, 25],
        ['01.22', 571, 393, 17, 25],
        ['01.23', 830, 1072, 25, 34],
        ['01.24', 1287, 1965, 41, 38],
        ['01.25', 1975, 2684, 56, 49],
        ['01.26', 2744, 5794, 80, 51],
        ['01.27', 4515, 6973, 106, 60],
        ['01.28', 5974, 9239, 132, 103],
        ['01.29', 7711, 12167, 170, 124],
        ['01.30', 9692, 15238, 213, 171],
    ]
    # data=json.dumps(data)
    return render(request, 'myapp/index.html',locals())


def add_city(request):
    data=spider.catch_city()
    for i in data:
        detail=Detail()
        detail.date=i[0]
        detail.province=i[1]
        detail.city=i[2]
        detail.nowConfirm=i[3]
        detail.confirm=i[4]
        detail.suspect=i[5]
        detail.dead=i[6]
        detail.heal=i[7]
        detail.save()
    return HttpResponse('数据插入成功')


def main(request):
    map_data = Detail.objects.values('province').annotate(value=Sum('confirm'))
    eighth_data=(Detail.objects.values('province').annotate(value=Sum('confirm'))).order_by('-value')[1:9]
    last_info=History.objects.last()
    heal=last_info.confirm-last_info.dead
    history_list=History.objects.all()
    hotsearch_list=HotSearch.objects.all()

    # return render(request, 'myapp/main.html',locals())
    return render(request, 'myapp/index2.html',locals())


def time(request):
    return HttpResponse(get_time())


def get_map(request):
    eighth_data = (Detail.objects.values('province').annotate(value=Sum('confirm'))).order_by('-value')[1:9]
    print(eighth_data)
    # print(type(data))
    return HttpResponse('获取数据成功')


def image(request):
    return render(request, 'myapp/image.html',locals())