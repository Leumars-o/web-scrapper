#!/usr/bin/python3

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver_location = "/snap/bin/chromium.chromedriver"
binary_location = "/usr/bin/chromium-browser"

options = webdriver.ChromeOptions()
options.binary_location = binary_location

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://imdb.com")
print(driver.page_source.encode("utf-8"))
driver.quit()
