from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def open_browser():

    options = Options()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    return driver

def load_page(driver, menu_url, wait_until):
    print("scraping ", menu_url, "started")

    driver.get(menu_url)
    
    # Wait until the element with tag 'h3' and class 'text-center' is loaded
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, wait_until))
        WebDriverWait(driver, 20).until(element_present)
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")


    soup = BeautifulSoup(driver.page_source, "html.parser")

    return soup

def close_driver(driver):
    driver.quit()  # Close the browser