import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import pickle
import time

def is_logged_in(driver):
    try:
        driver.get('https://www.storyblocks.com')
        driver.find_element(By.LINK_TEXT, "Join Now")
        return False
    except:
        return True
    
def logging_in(driver):
    driver.get('https://www.storyblocks.com/login') 
    username_field = driver.find_element(By.ID, "email")  
    password_field = driver.find_element(By.ID, "password")  
    email = os.getenv("WEB_EMAIL")
    password = os.getenv("WEB_PASSWORD")
    username_field.send_keys(email)  
    password_field.send_keys(password)  

    checkbox = driver.find_element(By.ID, "agreement-checkbox") 
    
    checkbox.click()

    password_field.send_keys(Keys.RETURN)  # Simulate pressing Enter to submit
    print('Login script finished\n')

def getCookie(driver):
    try:
        with open("cookies.pkl", "rb") as cookie_file:
            driver.get('https://www.storyblocks.com')       #need to get here for cookies
            cookies = pickle.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookies loaded!")
            driver.refresh()
    except:
        print("Who got my cookies?")

    if (not is_logged_in(driver)):
        print("Not logged in")
        logging_in(driver)
        cookies = driver.get_cookies()
        with open("cookies.pkl", "wb") as cookie_file:
            pickle.dump(cookies, cookie_file)

    cookies = driver.get_cookies()
    login_session_value = next(cookie['value'] for cookie in cookies if cookie['name'] == 'login_session')
    return login_session_value


def getID(driver, url):
    driver.get(url)
    try:
        script_tag = driver.find_element("xpath", '//script[@type="application/ld+json"]')
        json_content = script_tag.get_attribute("innerHTML")
        id = json.loads(json_content)[0]["identifier"]
        return {'pageFound': True, 'id': id}
    except:
        return {'pageFound': False, 'id': 0}
