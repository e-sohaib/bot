import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver = webdriver.Chrome()
url = 'https://www.fxblue.com/market-data/tools/seinments'
driver.get(url)
element = WebDriverWait(driver, 10)
print(driver.page_source)