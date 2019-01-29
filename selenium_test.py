import pandas as pd
import datetime
dict_data = {'2018-12-30': 1301, '2018-12-31': 1210, '2019-01-01': 1117, '2019-01-02': 1374, '2019-01-03': 1504, '2019-01-04': 1655, '2019-01-05': 1377, '2019-01-06': 1348, '2019-01-07': 1351, '2019-01-08': 1432, '2019-01-09': 1446, '2019-01-10': 1454, '2019-01-11': 1363, '2019-01-12': 1367, '2019-01-13': 1332, '2019-01-14': 1477, '2019-01-15': 1282, '2019-01-16': 1338, '2019-01-17': 1262, '2019-01-18': 1337, '2019-01-19': 1141, '2019-01-20': 1223, '2019-01-21': 1314, '2019-01-22': 1297, '2019-01-23': 1298, '2019-01-24': 1324, '2019-01-25': 1575, '2019-01-26': 1322, '2019-01-27': 1317}
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

# date = '2018'
# index_data = 100
# dict_data[date] = dict_data.get(date,0) + index_data
# print(dict_data)
# print(dict_data)
# writer = pd.ExcelWriter('test.xlsx')
# sheet_1 = pd.DataFrame(dict_data,index=[0]).T
# # print(sheet_1)
# sheet_1.to_excel(writer, sheet_name=u'data')
# writer.close()

# print(pd.DataFrame.from_dict(dict_data,orient='index').T)
'''
start_time = '2018-11-01'
end_time = '2018-12-31'
start_date = datetime.datetime.strptime(start_time, '%Y-%m-%d')
end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d')
temp_date = start_date + datetime.timedelta(days=300)
print(temp_date)
all_days = (end_date - start_date).days
print(all_days)
'''


option = webdriver.ChromeOptions()
option.add_argument('lang=zh_CN.UTF-8')
option.add_argument("User-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/71.0.3578.98 Safari/537.36'")
driver = webdriver.Chrome('C:/Users/seanz/Downloads/chromedriver.exe',chrome_options=option)
url1 = 'https://passport.baidu.com/v2/?login'
url2 = 'http://index.baidu.com'
driver.get(url1)
time.sleep(8)
driver.get(url2)
time.sleep(1)
# 写入关键词
driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").clear()
keyword = u"车祸"
driver.find_element_by_xpath("//*[@id='search-input-form']/input[3]").send_keys(keyword)
driver.find_element_by_css_selector('div.search-input-operate').click()
# time.sleep(2)
# driver.maximize_window()
driver.set_window_size(1500, 900)

driver.find_elements_by_xpath('//*[@class="index-region"]')[0].click()
province = driver.find_elements_by_css_selector('div.provinces-group-box')

for i in province:
    print(i.text)
