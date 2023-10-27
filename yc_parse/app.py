import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from parsel import Selector
from config import chromedriverPath, YC_username, YC_password, filter_params


def setup_driver(chromedriverPath):
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        service = webdriver.ChromeService(executable_path=chromedriverPath)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except WebDriverException as e:
        print(f"Failed to set up the driver: {str(e)}")
        return None


def login(driver):
    try:
        driver.get('https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F')
        driver.find_element(By.ID, 'ycid-input').send_keys(YC_username)
        time.sleep(3)
        driver.find_element(By.ID, 'password-input').send_keys(YC_password)
        time.sleep(1.5)
        driver.find_element(By.CLASS_NAME, 'MuiButtonBase-root').click()
        time.sleep(2.5)
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Login failed: {str(e)}")


def navigate_to_filter_page(driver, filter_params):
    try:
        filter_url = f'https://www.workatastartup.com/companies?{filter_params}'
        driver.get(filter_url)
        time.sleep(5)
    except WebDriverException as e:
        print(f"Failed to navigate to the filter page: {str(e)}")


def extract_job_links(driver):
    try:
        sel = Selector(text=driver.page_source)
        job_links = sel.xpath('//a[contains(@href, "jobs")]/@href').getall()
        return job_links
    except (WebDriverException, AttributeError) as e:
        print(f"Failed to extract job links: {str(e)}")
        return []


def apply_to_job(driver, job_link):
    try:
        driver.get(job_link)
        time.sleep(5)
        apply_job_button = driver.find_element(By.LINK_TEXT, "Apply")
        apply_job_button.click()
        time.sleep(1)
        input_text = driver.find_element(By.TAG_NAME, 'textarea')
        input_text.send_keys(
            'I can Design and implement core data infra + pipelines. Help prototype and scale datasets for both model training and finetuning. Work closely with the rest of the team as we build and iterate on product.')
        time.sleep(2)
        send_button = driver.find_element(By.XPATH, '//button[text()="Send"]')
        send_button.click()
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Failed to apply to the job: {str(e)}")


def main(chromedriverPath):
    try:
        driver = setup_driver(chromedriverPath)
        time.sleep(5)
        try:
            login(driver)
            print("Logged in successfully.")
        except Exception as e:
            print(f"Failed to log in: {str(e)}")
        time.sleep(2)
        try:
            navigate_to_filter_page(driver, filter_params)
            print("Navigated to the filter page successfully.")

            try:
                job_links = extract_job_links(driver)

                if job_links:
                    apply_to_job(driver, job_links[2])
                    print("Applied to a job successfully.")
                else:
                    print("No job links found.")
            except Exception as e:
                print(f"Failed to extract job links: {str(e)}")
        except Exception as e:
            print(f"Failed to navigate to the filter page: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main(chromedriverPath)
    # print(chromedriverPath)
