from PIL import Image
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(20)
driver.get(
    'file:///home/runner/work/covid19-rating-graph/covid19-rating-graph/ogp.html')
driver.save_screenshot("img/ogp_bef.png")
driver.quit()

im = Image.open('img/ogp_bef.png')
im.crop((101, 0, 949, 445)).save('img/ogp.png', quality=95)
