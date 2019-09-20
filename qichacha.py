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
import math, re


class AutomateChaCha:

    username: str = '15918750018'
    password: str = 'a123456789'
    login_show_url: str = 'https://www.qichacha.com/user_login?back=%2F'
    home_url: str = 'https://www.qichacha.com/'
    cookies: dict = {}
    chrome_options: object

    def __init__(self):
        self.chrome_options = Options()
        self.browser = webdriver.Chrome(options=self.chrome_options)

    def login(self):
        """
        首先跳到登陆页面
        """
        self.browser.get(self.login_show_url)
        self.browser.find_element_by_xpath('//*[@id = "normalLogin"]').click()  # 转到登录界面
        self.browser.find_element_by_xpath(' // *[ @ id = "nameNormal"]').send_keys(self.username)  # 账号
        self.browser.find_element_by_xpath('// *[ @ id = "pwdNormal"]').send_keys(self.password)  # 密码
        time.sleep(3)

    def search_data(self, keyword: str):
        pass

    def download_excel(self):
        pass

    def data_import(self):
        pass

    def data_export(self):
        pass

    def combination_keyword(self):
        pass

