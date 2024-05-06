import csv
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def extract_group_id(group_url):
    parts = group_url.split('/')
    group_index = parts.index('groups')
    group_id = parts[group_index + 1]
    return group_id

def extract_user_id(messenger_url):
    url = messenger_url.split("https://www.facebook.com/messages/t/")
    if len(url) > 1 and len(url[1]) > 6:
        return url[1].replace("/", "")
    else:
        return None

def open_tab_with_url(driver, url):
    driver.execute_script("window.open('{}');".format(url))
    time.sleep(2)
def send_message(driver, link):
    try:
        print("This is link:", link)
        driver.get(url=link)
        driver.implicitly_wait(1)
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Message']"))).click()
        time.sleep(5)
        driver.implicitly_wait(1)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Message']"))).send_keys("Hello, Let's Test this?")
        time.sleep(5)
        driver.implicitly_wait(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Press Enter to send']"))).click()
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Close chat']"))).click()
        driver.implicitly_wait(10)
    except Exception as e:
        print("An error occurred:", e)
def initialize_driver():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-tracking-protection")
    options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

    driver = uc.Chrome(options=options)
    return driver

try:
    group_url = "https://www.facebook.com/groups/6647478202045813/members"
    group_id = extract_group_id(group_url)
    url = "https://www.facebook.com/login.php"
    driver = initialize_driver()
    driver.get(url=url)
    driver.implicitly_wait(10)
    email = driver.find_element(By.ID, "email")
    email.send_keys("EMAIL")
    password = driver.find_element(By.ID, "pass")
    password.send_keys("PASSWORD")
    login_button = driver.find_element(By.ID, "loginbutton")
    login_button.click()
    time.sleep(5)
    driver.get(group_url)
    scroll_count = 2
    scroll = 0
    while scroll < scroll_count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        scroll += 1
    links = driver.find_elements(By.CLASS_NAME, "x1i10hfl")
    list_of_links=[]
    for link in links:
        href = link.get_attribute("href")
        if href==None:
            pass
        elif href and "https://www.facebook.com/groups/" in href and "/user/" in href:
             user_id = re.search(r"/user/(\d+)/", href)
             if user_id:
                if "contributions/?ref=member_leaderboard_contribution_points_link" in href:
                    pass
                else:
                    list_of_links.append(href)
                    
                 
    for item in list_of_links:
        print("This is link:",item)
        send_message(driver=driver,link=item)               
                
except NoSuchElementException as e:
    print("NoSuchElementException occurred:", e)
    ans = input("Exception Arrive: ")
except Exception as e:
    print("An error occurred:", e)
    ans = input("Exception Arive: ")
finally:
    if 'driver' in locals() or 'driver' in globals():
        input()
        driver.quit()