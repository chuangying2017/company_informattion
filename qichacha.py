from multiprocessing import Pool
import random
import requests
import time, datetime
from pyquery import PyQuery
import os, csv, json
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException
from selenium.webdriver import ActionChains
from urllib import parse
from model import create_all
import math, re, shutil
import openpyxl
import xlrd
import model


"""
企查查 数据查询 根据时间查询 每个小月查询100次
根据帐号每天 导出10次excel


"""


class AutomateChaCha:
    username: str = '15918750018'
    password: str = 'a123456789'
    login_show_url: str = 'https://www.qichacha.com/user_login?back=%2F'
    home_url: str = 'https://www.qichacha.com/'
    cookies: dict = {}
    chrome_options: object
    headers: dict = {
        "Cookie": "QCCSESSID=csb0md62ha6vhiim8l4c390q04; UM_distinctid=16d1fb70247240-08b2c06aeb5191-7373e61-2a3000-16d1fb702488d3; _uab_collina=156819515061093531026689; acw_tc=b7f0d81615681951514382151eecbb97cf3adfd30dfb42bdfdf6ba931e; zg_did=%7B%22did%22%3A%20%2216d1fb703a334a-010890d039fa5e-7373e61-2a3000-16d1fb703a470e%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1569323239,1569374069,1569465437; hasShow=1; CNZZDATA1254842228=1885778088-1569322378-https%253A%252F%252Fsp0.baidu.com%252F%7C1569484158; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1569484450; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201569483637466%2C%22updated%22%3A%201569485555864%2C%22info%22%3A%201569323237898%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22a240b361c35797710baddf45be188ad5%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D",
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Host": "www.qichacha.com",
        "Referer": "https://www.qichacha.com/",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Sec-Fetch-User": "?1"
    }

    def __init__(self):
        pass
        # self.chrome_options = Options()
        # self.browser = webdriver.Chrome(options=self.chrome_options)

    def login(self):
        """
        首先跳到登陆页面
        """
        self.browser.get(self.login_show_url)
        self.browser.find_element_by_xpath('//*[@id="normalLogin"]').click()  # 转到登录界面
        self.browser.find_element_by_xpath(' //*[@id="nameNormal"]').send_keys(self.username)  # 账号
        self.browser.find_element_by_xpath('//*[@id="pwdNormal"]').send_keys(self.password)  # 密码
        time.sleep(3)
        button = self.browser.find_element_by_xpath('//*[@id="dom_id_one"]/div/div/span')
        # 开始拖动 perform()用来执行ActionChains中存储的行为
        action = ActionChains(self.browser)  # 实例化一个action对象
        action.click_and_hold(button).perform()  # 鼠标左键按下不放
        action.reset_actions()  # 清除之前的action
        ttt = [23, 81, 204]
        action.move_by_offset(xoffset=sum(ttt), yoffset=0).perform()  # 移动滑块
        # for i in ttt:
        #     action.move_by_offset(xoffset=i, yoffset=0).perform()  # 移动滑块
        #     action.reset_actions()
        #     time.sleep(0.4)
        action.release().perform()
        time.sleep(5)
        # 滑块，有刷新，有验证码
        # 取刷新,
        alert = self.browser.find_element_by_class_name('nc-lang-cnt').text
        if alert == "哎呀，出错了，点击刷新再来一次":
            print('日...!')
            while 1:
                while True:
                    self.browser.find_element_by_xpath('//*[@id="dom_id_one"]/div/span/a').click()
                    if button:
                        print('出现滑块')
                        break
                # 滑块
                button = self.browser.find_element_by_xpath('//*[@id="dom_id_one"]/div/div/span')
                action.click_and_hold(button).perform()  # 鼠标左键按下不放
                action.reset_actions()  # 清除之前的action
                for t in ttt:
                    action.move_by_offset(xoffset=t, yoffset=0).perform()
                    action.reset_actions()
                    time.sleep(0.4)
                action.release().perform()
                time.sleep(5)
                alert = self.browser.find_element_by_class_name('nc-lang-cnt').text
                if alert == "哎呀，出错了，点击刷新再来一次":
                    print('我日...又进不去')
                    break
        else:
            try:
                self.browser.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()  # 点击登录
                time.sleep(5)
                self.browser.find_element_by_xpath(
                    '//*[@id="bindwxModal"]/div/div/div/button/span[1]').click()  # 点×
                dictCookies = self.browser.get_cookies()
                print(dictCookies)
                jsonCookies = json.dumps(dictCookies)
                # 登录完成后,将cookies保存到本地文件
                with open("cookies.json", "w") as fp:
                    fp.write(jsonCookies)
                print('登录完成后......')
            except Exception as e:
                print(e, '出现异常啦')

    def search_data(self, keyword: str):
        pass

    def download_excel(self):
        pass

    def data_import(self):
        dir_path = r'E:\xls\not_import'
        source_path = r'E:\xls\already_import'
        res = []
        ls_res = self.path_easy(dir_path)
        data: list = []
        for path in ls_res:
            workbook = xlrd.open_workbook(filename=path)
            worksheet = workbook.sheet_by_index(0)
            nrows = worksheet.nrows
            for row in range(2, nrows):
                row = worksheet.row_values(row)
                data.append({
                    "company_name": row[0],
                    'status_quo': row[1],
                    'legal_representative': row[2],
                    'registered_capital': row[3],
                    'date_of_establishment': row[4],
                    'province': row[5],
                    'city': row[6],
                    'phone': row[7],
                    'more_phone': row[8],
                    'email': row[9],
                    'the_social_code': row[10],
                    'registration_number': row[11],
                    'register_number': row[12],
                    'organizing_institution_bar_code': row[13],
                    'contributors_in': row[14],
                    'type_of_business': row[15],
                    'industry': row[16],
                    'web_url': row[17],
                    'address': row[18],
                    'business_scope': row[19]
                })
            result = model.create_all(data)
            if result:
                shutil.move(path, source_path)
                data = []
                res.append(result)

        print(res)

    def path_easy(self, dir_path: str) -> list:
        ls: list = []
        for main_dir, subdir, file_name_list in os.walk(dir_path):
            for file in file_name_list:
                if file.find('xls') >= 0:
                    ls.append(os.path.join(main_dir, file))
        return ls

    def data_export(self):
        pass

    def combination_keyword(self):
        pass

    def admin_login(self):
        url = 'http://awpo.com.cn/admin/index'
        login_url = 'http://awpo.com.cn/auth/login'
        self.browser.delete_all_cookies()
        self.browser.get(login_url)
        with open('cookie_set_company.json', 'r') as pf:
            cookie = json.loads(pf.read())
            for dict_ in cookie:
                self.browser.add_cookie({
                    # 'domain': dict_.get('domain', ''),
                    'name': dict_.get('name', ''),
                    # 'expiry': dict_.get('expiry', ''),
                    'path': dict_.get('path', ''),
                    'value': dict_.get('value', ''),
                    'secure': dict_.get('secure', '')
                })
        self.browser.refresh()
        self.browser.get(url)
        print('success')

    def run(self):
        self.fetch_word()

    """
    手动分析请求， 进行解析请求的方式！
    需要请求的url
    """
    def operation_manual(self):
        pass

    def fetch_word(self):
        """
        获取 中文词组库
        :return:
        """
        if not os.path.exists('zuci.txt'):
            with open('city.txt', 'r') as citys, open('hanzi.txt', 'r') as cizu:
                city = citys.read().split(',')
                ci_ls = cizu.read().split(',')
            zuci_library: dict = {}
            for cs in city:
                pass


if __name__ == '__main__':
    chacha = AutomateChaCha()
    chacha.run()
