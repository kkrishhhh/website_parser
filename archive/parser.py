import requests
from bs4 import BeautifulSoup
import json
import sys

# Default URL 
URL = "https://quotes.toscrape.com/login"

# If user gives a URL when running the script, use that instead
if len(sys.argv) > 1:
    URL = sys.argv[1]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
response = requests.get(URL, headers=headers)

html = response.text
soup = BeautifulSoup(html, 'html.parser')


print(soup.prettify()[:1000])


input_tags = soup.find_all('input')
login_flow = {}

for tag in input_tags:
    input_type = tag.get('type', '')
    input_id = tag.get('id', '')
    input_class = tag.get('class', [])

    selector = 'input'
    if input_id:
        selector += f'#{input_id}'
    if input_class:
        selector += '.' + '.'.join(input_class)

    if input_type in ['text', 'email'] and (
    'user' in input_id.lower() or
    'email' in input_id.lower() or
    'email' in tag.get('name', '').lower() or
    'email' in tag.get('placeholder', '').lower()
):

        login_flow['EmailInput'] = selector
    elif input_type == 'password':
        login_flow['PasswordInput'] = selector
    elif input_type in ['submit', 'button'] or 'login' in tag.get('value', '').lower() or 'login' in ' '.join(input_class).lower():
        login_flow['SubmitButton'] = selector

button_tags = soup.find_all('button')
for tag in button_tags:
    button_text = tag.text.strip().lower()
    button_class = tag.get('class', [])
    
    selector = 'button'
    if tag.get('id'):
        selector += f'#{tag.get("id")}'
    if button_class:
        selector += '.' + '.'.join(button_class)

    if 'login' in button_text:
        login_flow['SubmitButton'] = selector
    elif 'add to cart' in button_text:
        login_flow['AddToCartButton'] = selector
    elif 'check' in button_text:
        login_flow['PincodeCheckButton'] = selector
    elif 'wishlist' in button_text:
        login_flow['WishlistButton'] = selector


a_tags = soup.find_all('a')
link_flows = {}

for tag in a_tags:
    link_text = tag.text.strip().lower()
    selector = 'a'
    if tag.get('class'):
        selector += '.' + '.'.join(tag['class'])

    if 'forgot' in link_text:
        link_flows['reset_password'] = {'ForgotPasswordLink': selector}
    elif 'sign up' in link_text or 'create account' in link_text:
        link_flows['signup_flow'] = {'SignUpLink': selector}
    elif 'home' in link_text:
        link_flows['nav_home'] = {'HomeLink': selector}
    elif 'contact' in link_text:
        link_flows['nav_contact_us'] = {'ContactLink': selector}
    elif 'download brochure' in link_text:
        link_flows['download_brochure'] = {'DownloadLink': selector}
    elif 'book demo' in link_text:
        link_flows['book_demo'] = {'DemoLink': selector}


final_output = {
    "login_flow": login_flow
}
final_output.update(link_flows)


print(json.dumps(final_output, indent=2))


domain = URL.split("//")[-1].split("/")[0].replace(".", "_")
filename = f"output_{domain}.json"

with open(filename, "w") as f:
    json.dump(final_output, f, indent=2)

