from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import json
import time

driver_path = r"C:\Users\Krishna thakur\Documents\website_parser\chromedriver-win64\chromedriver-win64\chromedriver.exe"
url = "https://www.thesouledstore.com/product/batman-3d-logo-tshirt?gte=1"

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)
time.sleep(5)

hostname = urlparse(url).hostname.replace(".", "_")
filename = f"selectors_{hostname}.json"

flows = {
    "login_flow": {},
    "create_account_flow": {},
    "search_flow": {},
    "terms_of_use": {},
    "nav_home": {},
    "footer_links": {},
    "help_flow": {},
    "other": {}
}

elements = driver.find_elements(By.XPATH, "//*")

for el in elements:
    try:
        text = el.text.strip().lower()
        if not text or len(text) > 100:
            continue

        selector = ""
        if el.get_attribute("id"):
            selector = f"{el.tag_name}#{el.get_attribute('id')}"
        elif el.get_attribute("name"):
            selector = f"{el.tag_name}[name='{el.get_attribute('name')}']"
        elif el.get_attribute("class"):
            class_name = el.get_attribute("class").strip().split()[0]
            selector = f"{el.tag_name}.{class_name}"
        else:
            continue

        # Match flows
        if any(x in text for x in ["email", "mobile", "otp", "login", "sign in"]):
            flows["login_flow"][text] = selector
        elif any(x in text for x in ["create account", "sign up", "new to flipkart"]):
            flows["create_account_flow"][text] = selector
        elif "search" in text or el.get_attribute("name") == "q":
            flows["search_flow"][text or "search"] = selector
        elif any(x in text for x in ["terms", "privacy", "policy", "conditions"]):
            flows["terms_of_use"][text] = selector
        elif any(x in text for x in ["explore", "home", "offer zone", "flights"]):
            flows["nav_home"][text] = selector
        elif any(x in text for x in ["contact", "about", "careers", "faq"]):
            flows["footer_links"][text] = selector
        elif any(x in text for x in ["help center", "support", "customer care", "help"]):
            flows["help_flow"][text] = selector
        else:
            flows["other"][text] = selector

    except Exception:
        continue

driver.quit()


with open(filename, "w", encoding="utf-8") as f:
    json.dump(flows, f, indent=2, ensure_ascii=False)

print(f"Selector JSON saved as {filename}")
