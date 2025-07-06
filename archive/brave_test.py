from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
driver_path = r"C:\Users\Krishna thakur\Documents\website_parser\chromedriver-win64\chromedriver-win64\chromedriver.exe"

options = Options()
options.binary_location = brave_path

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.flipkart.com/account/login")
print("Opened:", driver.title)

driver.quit()
