from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

driver_path = r"C:\Users\Krishna thakur\Documents\website_parser\chromedriver-win64\chromedriver-win64\chromedriver.exe"
options = Options()

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.thesouledstore.com/product/batman-3d-logo-tshirt?gte=1")
time.sleep(5)

# Get all elements with any tag
elements = driver.find_elements(By.XPATH, "//*")

for element in elements:
    text = element.text.strip()
    if text:
        print(f"{element.tag_name}: {text}")

driver.quit()
