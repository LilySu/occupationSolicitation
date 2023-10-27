import time

from parsel import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config import YC_password, YC_username, chromedriverPath, filter_params


def setup_driver(chromedriverPath):
    """
    Set up a Selenium web driver for Chrome.

    Args:
        chromedriverPath (str): Path to the Chrome WebDriver executable.

    Returns:
        webdriver.Chrome: A configured Chrome web driver instance.
    """
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
    """
    Log in to the Y Combinator website using provided credentials.

    Args:
        driver (webdriver.Chrome): A configured Chrome web driver instance.
    """
    try:
        driver.get(
            "https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2F"
        )
        driver.find_element(By.ID, "ycid-input").send_keys(YC_username)
        time.sleep(3)
        driver.find_element(By.ID, "password-input").send_keys(YC_password)
        time.sleep(1.5)
        driver.find_element(By.CLASS_NAME, "MuiButtonBase-root").click()
        time.sleep(2.5)
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Login failed: {str(e)}")


def navigate_to_filter_page(driver, filter_params):
    """
    Navigate to a filter page on the website.

    Args:
        driver (webdriver.Chrome): A configured Chrome web driver instance.
        filter_params (str): URL parameters for filtering the page.
    """
    try:
        filter_url = f"https://www.workatastartup.com/companies?{filter_params}"
        driver.get(filter_url)
        time.sleep(5)
    except WebDriverException as e:
        print(f"Failed to navigate to the filter page: {str(e)}")


def extract_job_links(driver):
    """
    Extracts a list of job listing urls from the current page.

    Args:
        driver (webdriver.Chrome): A configured Chrome web driver instance.

    Returns:
        list: A list of job links.
    """
    try:
        sel = Selector(text=driver.page_source)
        job_links = sel.xpath('//a[contains(@href, "jobs")]/@href').getall()
        return job_links
    except (WebDriverException, AttributeError) as e:
        print(f"Failed to extract job links: {str(e)}")
        return []


def apply_to_job(driver, job_link):
    """
    Apply to a job by clicking the "Apply" button and filling in the text box.

    Args:
        driver (webdriver.Chrome): A configured Chrome web driver instance.
        job_link (str): URL of the job to apply for.
    """
    try:
        driver.get(job_link)
        time.sleep(5)
        apply_job_button = driver.find_element(By.LINK_TEXT, "Apply")
        apply_job_button.click()
        time.sleep(1)
        input_text = driver.find_element(By.TAG_NAME, "textarea")
        input_text.send_keys(
            "I can Design and implement core data infra + pipelines. Help prototype and scale datasets for both model training and finetuning. Work closely with the rest of the team as we build and iterate on product."
        )
        time.sleep(2)
        send_button = driver.find_element(By.XPATH, '//button[text()="Send"]')
        send_button.click()
        return True
    except (WebDriverException, NoSuchElementException) as e:
        print(f"Failed to apply to the job: {str(e)}")
        return False


def main(chromedriverPath):
    """
    Main function to automate job application on the Y Combinator website.

    Args:
        chromedriverPath (str): Path to the Chrome WebDriver executable.
    """
    # Attempt to set up a web driver for Selenium using the specified chromedriverPath.
    try:
        driver = setup_driver(chromedriverPath)
        time.sleep(5)  # Pause for 5 seconds to ensure driver setup is complete.

        # Try to log in using the established driver.
        try:
            login(driver)
            print("Logged in successfully.")
        except Exception as e:
            print(f"Failed to log in: {str(e)}")

        time.sleep(4)  # Pause for 4 seconds.

        # Try to navigate to the filter page using the driver.
        try:
            navigate_to_filter_page(driver, filter_params)
            print("Navigated to the filter page successfully.")
            time.sleep(1)  # Pause for 1 seconds.

            # Scroll down to get all jobs
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            SCROLL_PAUSE_TIME = 2.5

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(7)  # Pause for 7 seconds.
            # Try to extract job links from the web page.
            try:
                job_links = extract_job_links(driver)
                print(len(job_links))
                time.sleep(2000)  # Pause for 2 seconds.
                if job_links:
                    # If job links are found, apply to a job (in this case, the third job link).
                    applied = apply_to_job(driver, job_links[3])
                    if applied:
                        print("Applied to a job successfully.")
                    else:
                        print("Already applied or something went wrong.")
                else:
                    print("No job links found.")
            except Exception as e:
                print(f"Failed to extract job links: {str(e)}")

        except Exception as e:
            print(f"Failed to navigate to the filter page: {str(e)}")

    # Handle exceptions by printing an error message.
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Ensure that the driver is properly closed or quit regardless of success or failure.
    finally:
        driver.quit()


if __name__ == "__main__":
    main(chromedriverPath)
    # print(chromedriverPath)