import csv
import random
from time import sleep

from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import config

# Login Start
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
service = webdriver.ChromeService(
    executable_path=r"C:\Users\User\git\occupationalSolicitation\newScrape\chromedriver.exe"
)
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(
    "https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F"
)
# driver.find_element("name", "q")
username = driver.find_element(By.ID, "ycid-input")
username.send_keys(parameters.linkedin_username)
sleep(3)

password = driver.find_element(By.ID, "password-input")
password.send_keys(parameters.linkedin_password)
sleep(1.5)

sign_in_button = driver.find_element(
    By.CLASS_NAME, "MuiButtonBase-root"
)  # sign - in -form__submit - button ')
sign_in_button.click()
sleep(2.5)
# Login Complete


# Navigate to Filter Page
driver.get(
    f"https://www.workatastartup.com/companies?demographic=any&hasEquity=any&hasSalary=any&industry=any&interviewProcess=any&jobType=any&layout=list-compact&locations=US&remote=yes&role=eng&role_type=ml&sortBy=created_desc&tab=any&usVisaNotRequired=any"
)
sleep(5)

sel = Selector(text=driver.page_source)
# Extract a list of job listings
job_link = sel.xpath('//a[contains(@href, "jobs")]/@href').getall()

print(job_link)

driver.get(job_link[1])

sleep(5)

apply_job_button = driver.find_element(By.LINK_TEXT, "Apply")
apply_job_button.click()

sleep(1)
input_text = driver.find_element(By.TAG_NAME, "textarea")
input_text.send_keys(
    "I can Design and implement core data infra + pipelines. Help prototype and scale datasets for both model training and finetuning.Work closely with the rest of the team as we build and iterate on product."
)
sleep(2)
# send_button = driver.find_element(By.XPATH, '//button[text()="Send"]')
# send_button.click()
