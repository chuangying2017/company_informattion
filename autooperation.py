from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

server = 'http://localhost:4723/wd/hub'
desired = {
  "platformName": "Android",
  "deviceName": "V1832A",
  "appActivity": "com.shine.ui.home.HomeActivity",
  "appPackage": "com.shizhuang.duapp"
}

driver = webdriver.Remote(server, desired)
