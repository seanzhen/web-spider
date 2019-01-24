import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import json

url = 'https://movie.douban.com/top250'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Host':'movie.douban.com'
}
for i in range(10):
    link = url
    # print(link)
    s = {'start': str(i*25)}
    # print(s)
    r = requests.post(url=link,data=s,headers = headers,timeout = 1)
    # print(r.url)
    print(str(i + 1), "页响应状态码:", r.status_code)
    # print(r.text)
    soup = BeautifulSoup(r.text,'lxml')
    content = soup.find_all('div',class_='hd')
    for j in content:
        # for string in j.a.stripped_strings:
        #     s = "".join(string.split())
        #     print(s.replace('/',' ').lstrip())
        # print(index)
        # print(''.join((j.a.text.replace('/',' ').lstrip()).split()))
        print(j.a.span.text.strip())


