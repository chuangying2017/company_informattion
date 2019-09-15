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
from model import create_all


headers = {
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

storage_ship = ["TYCID=2a0403d0d78111e99804e59d2a3844cf; undefined=2a0403d0d78111e99804e59d2a3844cf; ssuid=8056998828; bannerFlag=undefined; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568528539; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568530369; _ga=GA1.2.1465036504.1568528539; _gid=GA1.2.1393168162.1568528539; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522zzas%2522%252C%2522integrity%2522%253A%252214%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODUyODU2OCwiZXhwIjoxNjAwMDY0NTY4fQ.2zpz1j7AyKVSnXe-TYYTG4vmNKnr22ylrWEHtlCGWghKwPtzKmb4EABlZnai4O97irDRl0CHsBhnXp4B3kAZRA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213502571647%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzUwMjU3MTY0NyIsImlhdCI6MTU2ODUyODU2OCwiZXhwIjoxNjAwMDY0NTY4fQ.2zpz1j7AyKVSnXe-TYYTG4vmNKnr22ylrWEHtlCGWghKwPtzKmb4EABlZnai4O97irDRl0CHsBhnXp4B3kAZRA; RTYCID=3c1c0812ef8a4e1a9b26305e2bd4b90f; CT_TYCID=3cbc15c5ac9c4ca586da27c93ae78b05; cloud_token=146edfd12b6846ebb869228727e8a116; _gat_gtag_UA_123487620_1=1"]
cookie = "jsid=SEM-BAIDU-PZ1907-SY-000100; TYCID=7c336120d63a11e98afab7d0efc933dc; undefined=7c336120d63a11e98afab7d0efc933dc; ssuid=5047837311; _ga=GA1.2.1112942777.1568388228; _gid=GA1.2.1772276711.1568388228; RTYCID=3458f9f2865e46d7965c1735566be63d; CT_TYCID=e3d02897d29f4c40b30606019bc854e0; aliyungf_tc=AQAAAPZK/hcAcwcAEMEhO3NnHow+WPEB; csrfToken=n1vX-rtUEHYfU6x1531uR2f_; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%25B3%2595%25E7%25B1%25B3%25E5%2585%258B%25C2%25B7%25E8%25A9%25B9%25E6%25A3%25AE%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A0%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODM5MzE1MSwiZXhwIjoxNTk5OTI5MTUxfQ.CtGIrRcSTJfw18XehIDC_BrubHcbhEQRfuLs5_x3u86kjRC0MJucGi5Wj2TPg4yX-oydZzQb3_pFn89eyfAMfw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213059551109%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzA1OTU1MTEwOSIsImlhdCI6MTU2ODM5MzE1MSwiZXhwIjoxNTk5OTI5MTUxfQ.CtGIrRcSTJfw18XehIDC_BrubHcbhEQRfuLs5_x3u86kjRC0MJucGi5Wj2TPg4yX-oydZzQb3_pFn89eyfAMfw; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568388228,1568393135,1568423352,1568511245; cloud_token=26f67e422ed84c49966a5e1946701f1c; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568511303; bannerFlag=true"
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
    headers['Cookie'] = fetch_rand_value(storage_ship)
    res = requests.get(url, headers=headers)

    if res.status_code in (200, 201):
        jq = PyQuery(res.text)
        file = open('test.txt', 'w', encoding='utf-8')
        file.write(res.text)
        file.close()
        # data: dict = {}
        # sv_search_container = jq("div.header-block-container .sv-search-container")
        # all_element = sv_search_container.children()
        # for i in all_element:
        #     print()


def find_html() -> list:
    file = open('test.txt', 'r', encoding='utf-8')

    read = file.read()

    file.close()

    jq = PyQuery(read)

    sv_search_container = jq("div.header-block-container .sv-search-container")

    all_element = sv_search_container.children()

    stogre_list: list = []

    for k, element in enumerate(all_element.items()):
        content_div = element.find('.content')
        header_div = content_div.find('.header')
        company_name = header_div.find('a').text()
        status_quo = header_div.find('div').text()
        info_row = content_div.find('.info.row.text-ellipsis').children()
        legal_representative = info_row.eq(0).find('a').text()
        registered_capital = info_row.eq(1).find('span').text()
        date_of_establishment = info_row.eq(2).find('span').text()
        contact_info = content_div.find('.contact.row')

        phone, email = ('', '')
        if contact_info:
            str_list = contact_info.children()
            try:
                for key, j in enumerate(str_list.items()):
                    script = j.find('script').text()
                    # common_list = eval(script)
                    if script:
                        script = eval(script)
                        script = ','.join(script)
                    if key > 0:
                        email = script
                        # email = ','.join(common_list)
                    else:
                        phone = script
                        # phone = ','.join(common_list)
            except Exception as e:
                print(e)

        match_address_info = content_div.find('.match.row.text-ellipsis').children()
        register_address = ''
        if match_address_info:
            register_address = match_address_info.eq(2).text()
        stogre_list.append({
            "company_name": company_name,
            "status_quo": status_quo,
            "legal_representative": legal_representative,
            "registered_capital": registered_capital,
            "date_of_establishment": date_of_establishment,
            "phone": phone,
            "email": email,
            "register_address": register_address
        })
    return stogre_list


def fetch_rand_value(storage_list: list = []) -> str:

    ls_len = storage_list.__len__()

    values = random.randint(1, ls_len)

    return storage_list[values - 1]


if __name__ == '__main__':
    # search_key = parse.quote("东莞")
    #
    # fetch_data("https://www.tianyancha.com/search?key=" + search_key)
    res = find_html()
    insert_res = create_all(res)
    print(insert_res)

