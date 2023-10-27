from selenium.webdriver.common.by import By

import parameters
from time import sleep
from selenium import webdriver

# find_element(By.ID, "id")
# find_element(By.NAME, "name")
# find_element(By.XPATH, "xpath")
# find_element(By.LINK_TEXT, "link text")
# find_element(By.PARTIAL_LINK_TEXT, "partial link text")
# find_element(By.TAG_NAME, "tag name")
# find_element(By.CLASS_NAME, "class name")
# find_element(By.CSS_SELECTOR, "css selector")
def login_to_yc():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    service = webdriver.ChromeService(
        executable_path=r'C:\Users\User\git\occupationalSolicitation\newScrape\chromedriver.exe')
    # driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=service,options=options)
    driver.get('https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F')
    # driver.find_element("name", "q")
    username = driver.find_element(By.ID,'ycid-input')
    username.send_keys(parameters.linkedin_username)
    sleep(3)

    password = driver.find_element(By.ID,'password-input')
    password.send_keys(parameters.linkedin_password)
    sleep(1.5)

    sign_in_button = driver.find_element(By.CLASS_NAME,'MuiButtonBase-root')# sign - in -form__submit - button ')
    sign_in_button.click()
    sleep(2.5)
    return