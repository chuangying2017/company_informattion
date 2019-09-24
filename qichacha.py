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


class AutomateChaCha:
    username: str = '15918750018'
    password: str = 'a123456789'
    login_show_url: str = 'https://www.qichacha.com/user_login?back=%2F'
    home_url: str = 'https://www.qichacha.com/'
    cookies: dict = {}
    chrome_options: object

    def __init__(self):pass
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
        a = 0
        for i in ttt:
            action.move_by_offset(xoffset=i, yoffset=0).perform()  # 移动滑块
            action.reset_actions()
            time.sleep(0.4)
            a += i
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
                    a += t
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
                ls.append(os.path.join(main_dir, file))
        return ls

    def data_export(self):
        pass

    def combination_keyword(self):
        pass

    def run(self):
        self.data_import()


if __name__ == '__main__':
    chacha = AutomateChaCha()
    chacha.run()
