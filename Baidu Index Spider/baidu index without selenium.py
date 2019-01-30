# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 16:33:00 2019

@author: Sean Zhen
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import os
import pandas as pd
import datetime
import time
import json
from config import CITY_CODE

# province_code = PROVINCE_CODE
city_code = CITY_CODE
# print(city_code)

headers = {
    'Host': 'index.baidu.com',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

start_time = '2018-01-01'
end_time = '2019-01-01'
start_date = datetime.datetime.strptime(start_time, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d')
COOKIES = ''
# cookies = [{'name': cookie.split('=')[0],
#             'value': cookie.split('=')[1]}
#            for cookie in COOKIES.replace(' ', '').split(';')]
# print(cookies)

def get_time_range_list(start_date, end_date):
    """
    max 6 months
    """
    date_range_list = []
    while 1:
        # datetime.timedelta对象代表两个时间之间的时间差
        # print(start_date)
        temp_date = start_date + datetime.timedelta(days=300)
        if temp_date >= end_date:
            all_days = (end_date - start_date).days
            date_range_list.append((start_date, end_date))
            return date_range_list
        date_range_list.append((start_date, temp_date))
        start_date = temp_date + datetime.timedelta(days=1)

def decrypt(key,data):
    m = list(key)
    d = dict(zip(m[:len(m) // 2], m[len(m) // 2::]))
    str_list =  ''.join(map(lambda x: d[x], data)).split(',')
    print(str_list)
    data_list = []
    for s in str_list:
        try:
            data_list.append(int(s))
        except:
            data_list.append(0)
    return data_list

def format_data(formated_data,data,s):
    time_len = len(data)
    cur_date = s
    for i in range(time_len):
        date = cur_date.strftime('%Y-%m-%d')
        formated_data[date] = data[i]
        cur_date += datetime.timedelta(days=1)
    return formated_data

time_list = get_time_range_list(start_date,end_date)

keyword_list = ["口罩",'aqi','交通事故','空气质量']#["车祸","雾霾","pm2.5","堵车","航班延误"]

city_list = ['全国','深圳','广州','北京','上海','河北','山西','天津','内蒙古','河南','湖北','湖南']

writer = pd.ExcelWriter('BaiduIndexData-2.xlsx')

for keyword in keyword_list:
    print(keyword)
    city_data = {}
    for city in city_list:
        city_data[city] = {}
        print(city)
        for s,e in time_list:
            # print(s,e)
            request_args = {
                'word': keyword,
                'startDate': s,
                'endDate': e,
                'area': city_code[city],
            }
            url1 ='http://index.baidu.com/api/SearchApi/index?' + urlencode(request_args)
            headers['Cookie'] = COOKIES
            response = requests.get(url1, headers=headers)
            if response.status_code == 200:
                html1 = response.text
            else:
                print(response.status_code)
                break
            html1_data = json.loads(html1)
            # print(data)
            uniqid = html1_data['data']['uniqid']
            # print(uniqid)
            # encrypt_data = []
            # for i in data['data']['userIndexes']:
            #     encrypt_data.append(i)
            # print(data['data']['userIndexes']['all']['data'])
            encrypt_data = html1_data['data']['userIndexes'][0]['all']['data']
            # print(encrypt_data)
            url2 = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqid
            response2 = requests.get(url2, headers=headers)
            html2 = response2.text
            html2_data = json.loads(html2)
            key = html2_data['data']
            # print(key)
            decrypt_data = decrypt(key,encrypt_data)
            # print(len(decrypt_data))
            print(decrypt_data)
            format_data(city_data[city],decrypt_data,s)

    sheet_1 = pd.DataFrame.from_dict(city_data)
    sheet_1.to_excel(writer, sheet_name=keyword)

writer.close()



