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
    # "Cookie": "QCCSESSID=csb0md62ha6vhiim8l4c390q04; UM_distinctid=16d1fb70247240-08b2c06aeb5191-7373e61-2a3000-16d1fb702488d3; CNZZDATA1254842228=1401409538-1568191378-https%253A%252F%252Fsp0.baidu.com%252F%7C1568191378; hasShow=1; _uab_collina=156819515061093531026689; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1568195151; acw_tc=b7f0d81615681951514382151eecbb97cf3adfd30dfb42bdfdf6ba931e; zg_did=%7B%22did%22%3A%20%2216d1fb703a334a-010890d039fa5e-7373e61-2a3000-16d1fb703a470e%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201568195150760%2C%22updated%22%3A%201568195379442%2C%22info%22%3A%201568195150763%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22sp0.baidu.com%22%2C%22cuid%22%3A%20%22a240b361c35797710baddf45be188ad5%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1568195380",
    "Cookie": "aliyungf_tc=AQAAAJtm2C2BngAAbkVK3+R1a0QWsqjp; ssuid=1889627566; csrfToken=16MKdtWuRjOizEDj7eQzJSLv; TYCID=7feee240d46811e9af47ddd61377535e; undefined=7feee240d46811e9af47ddd61377535e; _ga=GA1.2.2078788472.1568188090; _gid=GA1.2.218618058.1568188090; RTYCID=87b39eb998fd4989b701df715a6f2213; CT_TYCID=d5222bf3c6fc40a082dc2dccada12be9; jsid=SEM-BAIDU-PP-VI-301001; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568188090,1568193493; cloud_token=e6472ecac8204e24970776498d9114e6; bannerFlag=true; token=0fd388cfd859432bb90c83b92553540e; _utm=a38158a6523c422fa715a470714b72b8; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%25B3%2595%25E7%25B1%25B3%25E5%2585%258B%25C2%25B7%25E8%25A9%25B9%25E6%25A3%25AE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODkwMjIyNTQ4OCIsImlhdCI6MTU2ODE5NzAyNSwiZXhwIjoxNTk5NzMzMDI1fQ.FZn-1FasVe4vkMccMrIMpa0h5-F0Vj0ZYUCJAJ2RHbkYm8TWx5Iu16XORfyY4R-lxkFHWGN31yv1YRuS8ZUnnw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218902225488%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODkwMjIyNTQ4OCIsImlhdCI6MTU2ODE5NzAyNSwiZXhwIjoxNTk5NzMzMDI1fQ.FZn-1FasVe4vkMccMrIMpa0h5-F0Vj0ZYUCJAJ2RHbkYm8TWx5Iu16XORfyY4R-lxkFHWGN31yv1YRuS8ZUnnw; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568197026",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


class DatabaseOperation:

    def connect(self):
        pass

    def create(self):
        pass

    def update(self):
        pass


def fetch_data(url):
    global headers
    res = requests.get(url, headers=headers)
    print(res.status_code)
    print(res.text)


if __name__ == '__main__':
    search_key = parse.quote("东莞")

    fetch_data("https://www.tianyancha.com/search?key=" + search_key)
