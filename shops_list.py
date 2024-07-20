import requests

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import csv
from shared import open_browser, load_page, close_driver
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait



def scrap_company_data(soup, company_name):
        
    try:
        address_button = soup.find('button', {'data-item-id': 'address'})
        address = address_button.get('aria-label').replace('Address: ', '').strip()
    except AttributeError:
        address = None

    try:
        # Extract phone number
        phone_tag = soup.find('button', {'data-item-id': lambda x: x and 'phone' in x})
        phone_number = None
        if phone_tag:
            phone_div = phone_tag.find('div', {'class': 'Io6YTe fontBodyMedium kR99db'})
            if phone_div:
                phone_number = phone_div.get_text(strip=True)

    except AttributeError:
        phone_number = None

    try:        
        # Extract website
        website_tag = soup.find('a', {'class': 'CsEnBe'})
        website = website_tag.get('href') if website_tag else None
    except AttributeError:
        website = None

    return {
        'company_name': company_name,
        'address': address,
        'phone_number': phone_number,
        'website': website,
    }
    
def write_to_csv(data, filename='results.csv'):
    file_exists = os.path.isfile(filename)

    # Read existing links to avoid duplicates
    existing_links = set()
    if file_exists:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if file is not empty
            existing_links = {row[0] for row in reader}  # Collect existing slugs

    # Write new rows
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if the file did not exist
        if not file_exists:
            writer.writerow(['Name', 'Address', 'Phone', 'Website'])

        if data['company_name'] not in existing_links:
            writer.writerow([
                data['company_name'], 
                data['address'], 
                data['phone_number'], 
                data['website']
            ])


def click_on_shops(soup, driver):

    # Find all elements with the class "hfpxzc" in the BeautifulSoup object
    hfpxzc_elements = soup.find_all("a", class_="hfpxzc")
    
    # Iterate over each element
    for index, element in enumerate(hfpxzc_elements):
        try:
            # Find the corresponding element in the WebDriver by its index
            web_element = driver.find_elements(By.CLASS_NAME, 'hfpxzc')[index]
            
            # Click the element using the standard click method
            web_element.click()
            
            # Wait for the new content to load (if any)
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Find and print the text of the sibling element with the class "fontHeadlineSmall"
            parent_element = element.find_parent("div", class_="Nv2PK tH5CWc THOPZb")
            if parent_element:
                print("i'm here 1")
                font_headline_element = parent_element.find("div", class_="fontHeadlineSmall")
                if font_headline_element:

                    company_name = font_headline_element.get_text()

                    print("company is ", company_name)

                    detail_info = scrap_company_data(soup, company_name)
                    print(detail_info)

                    write_to_csv(detail_info)

            # Sleep for 10 seconds
            time.sleep(10)
        except Exception as e:
            print(f"An error occurred: {e}")
    

driver = open_browser()

shops_url = "https://www.google.com/maps/search/auto+repair+in+USA/@39.726212,-122.5272892,6z/data=!3m1!4b1?entry=ttu/"
soup = load_page(driver, shops_url, 'h1.fontTitleLarge.IFMGgb')
time.sleep(10)
soup = BeautifulSoup(driver.page_source, "html.parser")

scraped_data = click_on_shops(soup, driver)

# close_driver(driver)