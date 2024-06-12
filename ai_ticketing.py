import os
import requests
from bs4 import BeautifulSoup

url = "https://www.helpscout.com/blog/ai-ticketing/"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# List of CSS selectors
elements_to_scrape = [
    "#Content > p:nth-child(5)",
    "#Content > p:nth-child(6)",
    "#Content > p:nth-child(8)",
    "#Content > ul > li:nth-child(1) > p",
    "#Content > ul > li:nth-child(2) > p",
    "#Content > ul > li:nth-child(3) > p",
    "#Content > p:nth-child(10)",
    "#Content > p:nth-child(16)",
    "#Content > p:nth-child(17)",
    "#Content > p:nth-child(19)",
    "#Content > p:nth-child(20)",
    "#Content > h3:nth-child(22) > a",
    "#Content > p:nth-child(23)",
    "#Content > p:nth-child(24)",
    "#Content > p:nth-child(25)",
    "#Content > p:nth-child(26)",
    "#Content > h3:nth-child(27) > a",
    "#Content > p:nth-child(28)",
    "#Content > p:nth-child(30)",
    "#Content > p:nth-child(31)",
    "#Content > p:nth-child(32)",
    "#Content > h3:nth-child(34) > a",
    "#Content > p:nth-child(35)",
    "#Content > p:nth-child(37)",
    "#Content > p:nth-child(38)",
    "#Content > p:nth-child(39)",
    "#Content > h3:nth-child(41) > a",
    "#Content > p:nth-child(42)",
    "#Content > p:nth-child(44)",
    "#Content > p:nth-child(45)",
    "#Content > p:nth-child(46)",
    "#Content > h3:nth-child(48) > a",
    "#Content > p:nth-child(49)",
    "#Content > p:nth-child(51)",
    "#Content > p:nth-child(52)",
    "#Content > p:nth-child(53)",
    "#Content > h3:nth-child(55) > a",
    "#Content > p:nth-child(56)",
    "#Content > p:nth-child(58)",
    "#Content > p:nth-child(59)",
    "#Content > p:nth-child(60)",
    "#Content > h3:nth-child(61) > a",
    "#Content > p:nth-child(62)",
    "#Content > p:nth-child(64)",
    "#Content > p:nth-child(65)",
    "#Content > p:nth-child(66)",
    "#Content > p:nth-child(69)",
    "#Content > h3:nth-child(70)",
    "#Content > p:nth-child(71)",
    "#Content > h3:nth-child(72)",
    "#Content > p:nth-child(73)",
    "#Content > h3:nth-child(74)",
    "#Content > p:nth-child(75)",
    "#Content > p:nth-child(78)",
    "#Content > p:nth-child(79)"
]

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "ai_ticketing.txt")

with open(output_file, "w") as file:
    for css_selector in elements_to_scrape:
        element = soup.select_one(css_selector)
        if element:
            file.write(element.get_text() + '\n')
        else:
            file.write("element not found")

print(f" Text file saved in '{output_file}'")
