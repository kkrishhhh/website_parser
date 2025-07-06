from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

driver_path = r"C:\Users\Krishna thakur\Documents\website_parser\chromedriver-win64\chromedriver-win64\chromedriver.exe"

options = Options()
service = Service(driver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.thesouledstore.com/product/batman-3d-logo-tshirt?gte=1")

print("Opened:", driver.title)
driver.quit()
