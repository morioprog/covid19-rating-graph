import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://cards-dev.twitter.com/validator")

# ログイン
try:
    driver.implicitly_wait(20)
    username = driver.find_element_by_name('session[username_or_email]')
    password = driver.find_element_by_name('session[password]')
    username.send_keys(os.environ['TWITTER_EMAIL'])
    password.send_keys(os.environ['TWITTER_PASSWORD'])
    password.send_keys(Keys.ENTER)
except:
    pass

# 本人認証
try:
    driver.implicitly_wait(20)
    phone = driver.find_element_by_id('challenge_response')
    phone.send_keys(os.environ['TWITTER_PHONE'])
    phone.send_keys(Keys.ENTER)
except:
    pass

try:
    driver.implicitly_wait(20)
    update_url = driver.find_element_by_css_selector('input.FormControl')
    update_url.send_keys('https://morioprog.github.io/covid19-rating-graph/')
    update_url.send_keys(Keys.ENTER)
    time.sleep(20)  # ???
except:
    pass

driver.quit()
