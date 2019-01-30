# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 10:07:00 2019

@author: Sean Zhen
"""
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import datetime
import time
# 调用模拟鼠标点击的module
from selenium.webdriver.common.action_chains import ActionChains

def initial_brower(url):
    option = webdriver.ChromeOptions()
    option.add_argument('lang=zh_CN.UTF-8')
    option.add_argument("User-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
     Chrome/71.0.3578.98 Safari/537.36'")
    driver = webdriver.Chrome('C:/Users/seanz/Downloads/chromedriver.exe', chrome_options=option)
    driver.get(url)
    #用cookies登陆
    # driver.delete_all_cookies()
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    # driver.add_cookie(COOKIES)
    time.sleep(1)
    # driver.refresh()
    return driver

def get_time_range_list(start_date, end_date):
    """
    max 6 months
    """
    date_range_list = []
    while 1:
        # datetime.timedelta对象代表两个时间之间的时间差
        print(start_date)
        temp_date = start_date + datetime.timedelta(days=300)
        if temp_date >= end_date:
            all_days = (end_date - start_date).days
            date_range_list.append((start_date, end_date, all_days + 1))
            return date_range_list
        date_range_list.append((start_date, temp_date, 301))
        start_date = temp_date + datetime.timedelta(days=1)

def adjust_time_range(startdate, enddate):

    time.sleep(1)
    driver.find_elements_by_xpath('//*[@class="index-date-range-picker"]')[0].click()
    base_node = driver.find_element_by_xpath('//*[contains(@class, "index-date-range-picker-overlay-box") and \
        contains(@class, "tether-enabled")]')
    select_date(base_node, startdate)
    time.sleep(1)
    end_date_button = base_node.find_elements_by_xpath('.//*[@class="date-panel-wrapper"]')[1]
    end_date_button.click()
    select_date(base_node, enddate)
    time.sleep(1)
    base_node.find_element_by_xpath('.//*[@class="primary"]').click()
    # time.sleep(1)

def select_date(base_node, date):
    """
        select date
    """
    time.sleep(1)
    base_node = base_node.find_element_by_xpath('.//*[@class="right-wrapper" and not(contains(@style, "none"))]')
    next_year = base_node.find_element_by_xpath('.//*[@aria-label="下一年"]')
    pre_year = base_node.find_element_by_xpath('.//*[@aria-label="上一年"]')
    next_month = base_node.find_element_by_xpath('.//*[@aria-label="下个月"]')
    pre_month = base_node.find_element_by_xpath('.//*[@aria-label="上个月"]')
    cur_year = base_node.find_element_by_xpath('.//*[@class="veui-calendar-left"]//b').text
    cur_month = base_node.find_element_by_xpath('.//*[@class="veui-calendar-right"]//b').text
    diff_year = int(cur_year) - date.year
    diff_month = int(cur_month) - date.month
    if diff_year > 0:
        for _ in range(abs(diff_year)):
            pre_year.click()
    elif diff_year < 0:
        for _ in range(abs(diff_year)):
            next_year.click()

    if diff_month > 0:
        for _ in range(abs(diff_month)):
            pre_month.click()
    elif diff_month <0:
        for _ in range(abs(diff_month)):
            next_month.click()

    # time.sleep(1)
    base_node.find_elements_by_xpath('.//table//*[contains(@class, "veui-calendar-day")]')[date.day-1].click()

def get_data(dict_data,chart):
    date = chart.find_element_by_xpath('./div[2]/div[1]').text
    date = date.split(' ')[0]
    index_data = chart.find_element_by_xpath('./div[2]/div[2]/div[2]').text
    index_data = index_data.replace(',', '').strip(' ')
    dict_data[date] = dict_data.get(date, 0) + int(index_data)
    return dict_data

def data_loop(date_list):
    dict_data = {}
    for s,e,days in date_list:
        adjust_time_range(s,e)
        time.sleep(2)
        chart = driver.find_elements_by_xpath('//*[@class="index-trend-chart"]')[0]
        chart_size = chart.size
        move_step = days-1 #鼠标移动距离
        step = chart_size['width'] / move_step
        offset = {'x':step,'y':chart_size['height']-50}
        # 图片定位
        ActionChains(driver).move_to_element_with_offset(chart, 1, offset['y']).perform()
        get_data(dict_data, chart)
        time.sleep(0.5)
        for _ in range(days-1):
            time.sleep(0.5)
            ActionChains(driver).move_to_element_with_offset(chart,int(offset['x']),offset['y']).perform()
            offset['x'] += step
            get_data(dict_data,chart)
    return dict_data

def get_province_list():
    driver.find_elements_by_xpath('//*[@class="index-region"]')[0].click()
    province = driver.find_elements_by_css_selector('div.provinces-group-box')
    province_list = []
    for j in province:
        province_list.extend(j.find_elements_by_tag_name('span'))  # 省和直辖市列表
    return province_list

if __name__ == '__main__':
    url1 = 'https://passport.baidu.com/v2/?login'
    url2 = 'http://index.baidu.com'
    # 时间
    start_time = '2018-01-01'
    end_time = '2019-01-01'
    start_date = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    driver = initial_brower(url1)
    print('等待登陆')
    # time.sleep(8)
    # handles = driver.window_handles
    # driver.switch_to.window(handles[0])
    time.sleep(8)
    driver.get(url2)
    time.sleep(1)
    # 写入关键词
    keyword = ["车祸","雾霾","pm2.5","堵车","航班延误"]
    writer = pd.ExcelWriter('test.xlsx')
    for word in keyword:
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").clear()
        driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").send_keys(word)
        driver.find_element_by_css_selector('div.search-input-operate').click()
        driver.set_window_size(1500,900)
        '''
        ActionChains(driver).click(input1).perform()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,200)","")
        time.sleep(2)
        ActionChains(driver).move_by_offset(0,-80).perform()
        '''
        date_list = get_time_range_list(start_date,end_date)
        city_data = {}
        city_data[u'全国'] = data_loop(date_list)
        print(city_data)
        time.sleep(1)
        city_name = ['深圳','广州','北京','上海','河北','山西','天津','内蒙古']
        for i in city_name:
            print(i)
            province_list = get_province_list()
            if i == "深圳" or i == "广州":
                province_list[5].click()
                city = driver.find_element_by_css_selector('div.city-group-box')
                city_list = city.find_elements_by_tag_name('span')
                for j in city_list:
                    if i == j.text:
                        j.click()
                        city_data[i] = data_loop(date_list)
                        time.sleep(1)
                        driver.refresh()
                        break
            else:
                for k in province_list:
                    # print(k.text)
                    if i == k.text:
                        k.click()
                        city_data[i] = data_loop(date_list)
                        time.sleep(1)
                        driver.refresh()
                        break
        # 文件保存
        sheet_1 = pd.DataFrame.from_dict(city_data)
        sheet_1.to_excel(writer, sheet_name = word)
        driver.get(url2)
    time.sleep(1)
    driver.close()
    writer.close()