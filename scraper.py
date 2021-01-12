from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from time import sleep

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://sustainabledevelopment.un.org/partnership/browse/#")

driver.maximize_window()
# from selenium.webdriver.common.action_chains import ActionChains

# driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
# driver.implicitly_wait(3)
# button = driver.find_element_by_id("theMoreButton")
# driver.implicitly_wait(10)
# ActionChains(driver).move_to_element(button).click(button).perform()

driver.find_element_by_xpath("//*[@id='listing']")

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
# element = driver.find_element_by_id("theMoreButton")
# driver.execute_script("return arguments[0].scrollIntoView(true);", element)
# element.click()

# driver.set_window_size(1024, 768)
# driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
links = soup.find_all('a', class_="title", href=True)
#n = 2
# for j in range(0, 2):

for i in range(8, 26):
    try:
        top = driver.find_element_by_class_name('top')
        driver.execute_script('arguments[0].hidden="true";', top)
        header = driver.find_element_by_id('topBarArea')
        driver.execute_script('arguments[0].hidden="true";', header)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='listing']/div[" + str(i) + "]/a/div[3]/div[2]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        # driver.find_element_by_tag_name('body').send_keys(Keys.UP)
        #driver.execute_script("return arguments[0].scrollIntoView(true);", element)
        element.click()
    except:
        driver.quit()
    try:
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='intro']/div"))
        )
        print(element.text)
    except NoSuchElementException:
        driver.back()
        # element = WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[@id='theTopMenu']/a[2]/div"))
        # )
        # element.click()
    # try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div[1]/ul/li[2]/a'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='targets']"))
    )
    print(element.text)
    # except:
    #     driver.back()

    driver.back()

element = driver.find_element_by_id("theMoreButton")
driver.execute_script("return arguments[0].scrollIntoView(true);", element)
element.click()
for i in range(26, 30):
    # # print(link['href'])
    # try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='listing']/div[" + str(i) + "]/a/div[3]/div[2]"))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "intro"))
    )
    print(element.text)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div[1]/ul/li[2]/a'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='targets']"))
    )
    print(element.text)

    driver.back()

# driver.execute_script("window.scrollTo(0, window.scrollY + 100)")
    # driver.implicitly_wait(3)
    # button = driver.find_element_by_id("theMoreButton")
    # driver.implicitly_wait(10)
    # ActionChains(driver).move_to_element(button).click(button).perform()
    #n = n + 25

    # window_after = driver.window_handles[1]
    # driver.switch_to.window(window_after)
    # html = driver.page_source
    # soup = BeautifulSoup(html, 'lxml')
    # table = soup.findAll('div', class_="wrap")
    # print(table.prettify())
    # for x in table:
    #     print(x.find('p').text)
    # except:
    #     driver.quit()
