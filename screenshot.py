from PIL import Image
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get(
    'file:///home/runner/work/covid19-rating-graph/covid19-rating-graph/ogp.html')
time.sleep(20)  # ???
driver.save_screenshot("img/ogp_bef.png")
driver.quit()

im = Image.open('img/ogp_bef.png')
im.crop((0, 0, 838, 440)).save('img/ogp.png', quality=95)

im = Image.open('img/ogp_bef.png')
im.crop((0, 0, 640, 440)).save('img/graph.png', quality=95)
