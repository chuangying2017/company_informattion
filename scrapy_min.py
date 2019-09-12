from multiprocessing import Pool
import random
import requests
import time
from pyquery import PyQuery
import os, csv
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException
from urllib import parse


headers = {
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

storage_ship = ["TYCID=3f8b0270c7ba11e98d9c63cdd509ed77; undefined=3f8b0270c7ba11e98d9c63cdd509ed77; ssuid=8312427616; _ga=GA1.2.187922027.1566793846; aliyungf_tc=AQAAAI8nbQ/2jQUAjMPA35C6X4fCh59G; csrfToken=xhfuT12gjLbNLkh0gMMZhhXa; jsid=SEM-BAIDU-PZ1907-SY-000100; _gid=GA1.2.344159577.1568212438; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1566793849,1568212439; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%25B3%2595%25E7%25B1%25B3%25E5%2585%258B%25C2%25B7%25E8%25A9%25B9%25E6%25A3%25AE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODIxMjQ1MiwiZXhwIjoxNTk5NzQ4NDUyfQ.K8B9p5-SCBFqYNMfY61jK_DpbaW535p1ONPdvGvOl79_kS6-xVvCNCAs2awllFT7XWTOH7dfANC7E4iOKYRxcA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213059551109%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODIxMjQ1MiwiZXhwIjoxNTk5NzQ4NDUyfQ.K8B9p5-SCBFqYNMfY61jK_DpbaW535p1ONPdvGvOl79_kS6-xVvCNCAs2awllFT7XWTOH7dfANC7E4iOKYRxcA; token=72e3db6027f24483b9650854c5323ebb; _utm=bb35f6ac8bd4412daf9720e57a2c42a2; bannerFlag=true; RTYCID=e8c80efcd2ee4fc1a5d46e3cb6d55aec; CT_TYCID=2f3faa861a52429fac0fc40ec9241b8e; cloud_token=dd1f00c3f6144f66b2cc89c60e72f259; cloud_utm=9487e287043c4928b62e593dbc53b293; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568214484; _gat_gtag_UA_123487620_1=1"]
cookie = "aliyungf_tc=AQAAAMkGiz2OPQkAjMPA36u5u/6YUj7D; csrfToken=2cKc8qykIkxAwpSHHViWTCcm; jsid=SEM-BAIDU-PZ1907-SY-000100; TYCID=99c3cd00d4a111e99d0c97476c23ce2c; undefined=99c3cd00d4a111e99d0c97476c23ce2c; ssuid=9475157380; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568212629; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568213459; token=b975f255990a418ba1baa2004169fc17; _utm=27495e5e7d9d459cb9f2c1106c28475f; _ga=GA1.2.1832565216.1568212630; _gid=GA1.2.837782659.1568212630; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25221%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%25B3%2595%25E7%25B1%25B3%25E5%2585%258B%25C2%25B7%25E8%25A9%25B9%25E6%25A3%25AE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522new%2522%253A%25221%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODIxMjY3MiwiZXhwIjoxNTk5NzQ4NjcyfQ.j7Pq7rvLuK0jLolXAQ9UOW-4jEASqLrHP48ceYOt_kkE4J1gNkzizysss3aVPW_L4Vp0hunUG_nwR5weFfxjdw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213502571647%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODIxMjY3MiwiZXhwIjoxNTk5NzQ4NjcyfQ.j7Pq7rvLuK0jLolXAQ9UOW-4jEASqLrHP48ceYOt_kkE4J1gNkzizysss3aVPW_L4Vp0hunUG_nwR5weFfxjdw; _gat_gtag_UA_123487620_1=1"
storage_ship.append(cookie)


class DatabaseOperation:

    def connect(self):
        pass

    def create(self):
        pass

    def update(self):
        pass


def fetch_data(url):
    global headers, storage_ship
    headers['Cookie'] = storage_ship[0]
    res = requests.get(url, headers=headers)
    print(res.status_code)
    print(res.text)


def fetch_rand_value(storage_list: list = []) -> str:

    ls_len = storage_list.__len__()

    values = random.randint(1, ls_len)

    return storage_list[values - 1]


if __name__ == '__main__':
    search_key = parse.quote("东莞")

    fetch_data("https://www.tianyancha.com/search?key=" + search_key)

