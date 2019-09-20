import requests
import os, time, random
import lxml
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException


class LoginOperation:

    username: str = ''
    password: str = ''
    login_url: str = 'https://www.maybank2u.com.my/home/m2u/common/mbbLogin.do'
    login_show_url: str = 'https://www.maybank2u.com.my/home/m2u/common/login.do?sessionTimeout=true'

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self):
        try:

            browse = webdriver.Chrome()
            browse.get("https://www.baidu.com")
            input_ = browse.find_element_by_id('kw')
            input_.send_keys("商城")
            input_.send_keys(Keys.ENTER)
            wait = WebDriverWait(browse, 6)
        except Exception:
            print(Exception)
        finally:
            browse.close()


    def home(self):
        pass


if __name__ == "__main__":
    login = LoginOperation('Kelvinvoon98', 'Voon1998')
    login.login()
