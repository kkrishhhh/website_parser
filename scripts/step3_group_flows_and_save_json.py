from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

driver_path = r"C:\Users\Krishna thakur\Documents\website_parser\chromedriver-win64\chromedriver-win64\chromedriver.exe"
options = Options()
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.thesouledstore.com/product/batman-3d-logo-tshirt?gte=1")

elements = driver.find_elements("xpath", "//*")
flows = {
    "login_flow": [],
    "nav_links": [],
    "footer_links": [],
    "terms_of_use": [],
    "other": []
}

for el in elements:
    try:
        tag = el.tag_name
        text = el.text.strip()

        if not text:
            continue

        if any(word in text.lower() for word in ["email", "otp", "login", "account"]):
            flows["login_flow"].append({"tag": tag, "text": text})
        elif any(word in text.lower() for word in ["home", "electronics", "fashion", "appliances", "cart"]):
            flows["nav_links"].append({"tag": tag, "text": text})
        elif any(word in text.lower() for word in ["terms", "privacy"]):
            flows["terms_of_use"].append({"tag": tag, "text": text})
        elif any(word in text.lower() for word in ["about", "help", "contact", "careers"]):
            flows["footer_links"].append({"tag": tag, "text": text})
        else:
            flows["other"].append({"tag": tag, "text": text})

    except:
        pass

driver.quit()

with open("output_www.thesouledstore.com.json", "w", encoding="utf-8") as f:
    json.dump(flows, f, ensure_ascii=False, indent=2)

print("JSON saved.")
