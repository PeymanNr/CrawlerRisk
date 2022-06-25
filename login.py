from selenium import webdriver
from time import sleep


def get_cookie():
    driver = webdriver.Chrome()
    driver.implicitly_wait(50)
    driver.get("https://riskonline.ir/")

    login_step1 = driver.find_element_by_xpath('/html/body/header/div/div/div[3]/div/div[1]/a')
    login_step1.click()

    username = driver.find_element_by_xpath('//*[@id="username"]')
    username.clear()
    username.send_keys('pemi')

    password = driver.find_element_by_xpath('//*[@id="password"]')
    password.clear()
    password.send_keys('932319361')

    login_button = driver.find_element_by_xpath('//*[@id="customer_login"]/div[1]/form/p[3]/button')
    login_button.click()
    cookie = driver.get_cookie()
    driver.close()
    return cookie

