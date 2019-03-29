from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import util.util as Util

def exit(driver):
    button_exit = driver.find_element_by_class_name("exit")
    driver.implicitly_wait(1)
    button_logout = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "exit-select sign-out"))
    )
    button_logout.click()

def login():
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    driver.get("https://elearning.zbgedu.com/#studycenterIndex")

    try:
        input_name = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, "name"))
            )
        input_name.send_keys("13651652013")
        input_passwd = driver.find_element_by_id("password")
        input_passwd.send_keys("YstYsq971206")
        button_login = driver.find_element_by_id("login")
        button_login.click()

        driver.get("https://elearning.zbgedu.com/#myCourse/studyIn")

        try:
            button_messageBox_close = driver.find_element_by_xpath('//*[@id="layout"]/div[2]/div[6]/a/i')
            if button_messageBox_close:
                button_messageBox_close.click()
        except:
            print("no message box")

        button_CFA_basic = WebDriverWait(driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="scroller"]/div/div/div/ul/li[4]/a'))
            )
        button_CFA_basic.click()

        str = driver.page_source

        return str

    finally:
        # exit(driver)
        driver.close()
        pass
