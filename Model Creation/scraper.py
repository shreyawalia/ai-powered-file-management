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


driver.find_element_by_xpath("//*[@id='listing']")

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

links = soup.find_all('a', class_="title", href=True)


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
   
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div[1]/ul/li[2]/a'))
    )
    element.click()
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='targets']"))
    )
    print(element.text)


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

