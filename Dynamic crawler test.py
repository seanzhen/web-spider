import requests
from bs4 import BeautifulSoup
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# link = "https://api-zero.livere.com/v1/comments/list?callback=jQuery1124049866736766120545_1506309304525&limit=10&offset=1&repSeq=3871836&requestPath=%2Fv1%2Fcomments%2Flist&consumerSeq=1020&livereSeq=28583&smartloginSeq=5154&_=1506309304527"
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
#
# r = requests.get(link, headers= headers)
# print(r.status_code)
# # print (r.text)
# json_string = r.text
# json_string = json_string[json_string.find('{'):-2]
# json_data = json.loads(json_string)
# # print(json_data)
# comment = json_data['results']['parents']
# # print(comment)
# for i in comment:
#     print(i['content'])
# print(d.page_source)

d = webdriver.Chrome('C:/Users/seanz/Downloads/chromedriver.exe')
# 百度百科爬虫测试
d.get('https://baike.baidu.com/item/%E5%8F%A4%E5%85%B8%E9%9F%B3%E4%B9%90/106197?fr=aladdin')
'''
d.get("http://www.santostang.com/2018/07/04/hello-world/")

d.switch_to.frame(d.find_element_by_css_selector("iframe[title='livere']"))

# comment = d.find_element_by_css_selector('div.reply-content')
# content = comment.find_element_by_tag_name('p')
# print(content.text)
try:
    load_more = d.find_element_by_css_selector('div.more-wrapper')
    load_more.click()
except:
    pass
time.sleep(5) # 要设置时间才能点击后抓取下更多后评论
comments = d.find_elements_by_css_selector('div.reply-content')

for i in comments:
    content = i.find_element_by_tag_name('p')
    print(content.text)

# d.close()
'''
test = d.find_elements_by_css_selector('div.para.para')
for index,i in enumerate(test):
    try:
        c = i.find_elements_by_tag_name('a')
        for j in c:
            d = j.get_attribute('href')
            if j.text:
                print(j.text+' '+d+'\n')
        time.sleep(2)
        if index == 10:
            break
    except:
        pass


