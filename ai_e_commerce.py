import os
import requests
from bs4 import BeautifulSoup

url = "https://www.helpscout.com/blog/ai-for-ecommerce/"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# List of CSS selectors
elements_to_scrape = [
    "#gatsby-focus-wrapper > main > article > header > div > div > div.column.column--2-12-M.column--3-11-L > h1",
    "#Content > p:nth-child(1)",
    "#Content > p:nth-child(2)",
    "#Content > p:nth-child(5)",
    "#Content > p:nth-child(6)",
    "#Content > p:nth-child(7)",
    "#Content > p:nth-child(8)",
    "#Content > p:nth-child(11)",
    "#Content > p:nth-child(12)",
    "#Content > p:nth-child(13)",
    "#Content > p:nth-child(14)",
    "#Content > p:nth-child(15)",
    "#Content > p:nth-child(16)",
    "#Content > p:nth-child(19)",
    "#Content > h3:nth-child(20)",
    "#Content > p:nth-child(21)",
    "#Content > p:nth-child(22)",
    "#Content > h3:nth-child(23)",
    "#Content > p:nth-child(24)",
    "#Content > p:nth-child(25)",
    "#Content > h3:nth-child(26)",
    "#Content > p:nth-child(27)",
    "#Content > p:nth-child(30)",
    "#Content > h3:nth-child(31)",
    "#Content > p:nth-child(32)",
    "#Content > h3:nth-child(33)",
    "#Content > p:nth-child(34)",
    "#Content > h3:nth-child(35)",
    "#Content > p:nth-child(36)",
    "#Content > h3:nth-child(37)",
    "#Content > p:nth-child(38)",
    "#Content > h3:nth-child(39)",
    "#Content > p:nth-child(40)",
    "#Content > h3:nth-child(41)",
    "#Content > p:nth-child(42)",
    "#Content > h3:nth-child(47) > a",
    "#Content > p:nth-child(48) > i",
    "#Content > p:nth-child(50)",
    "#Content > p:nth-child(51)",
    "#Content > ul > li:nth-child(1) > p",
    "#Content > ul > li:nth-child(2) > p",
    "#Content > ul > li:nth-child(3) > p",
    "#Content > p:nth-child(54)",
    "#Content > p:nth-child(55)",
    "#Content > p:nth-child(56)",
    "#Content > h3:nth-child(58) > a",
    "#Content > p:nth-child(61)",
    "#Content > p:nth-child(62)",
    "#Content > p:nth-child(63)",
    "#Content > h3:nth-child(64) > a",
    "#Content > p:nth-child(65)",
    "#Content > p:nth-child(66)",
    "#Content > p:nth-child(67)",
    "#Content > p:nth-child(68)",
    "#Content > h3:nth-child(70)",
    "#Content > p:nth-child(71)",
    "#Content > p:nth-child(72)",
    "#Content > p:nth-child(73)",
    "#Content > p:nth-child(74)",
    "#Content > h3:nth-child(75)",
    "#Content > p:nth-child(76)",
    "#Content > p:nth-child(77)",
    "#Content > p:nth-child(74)",
    "#Content > p:nth-child(78)",
    "#Content > p:nth-child(79)",
    "#Content > p:nth-child(82)",
    "#Content > p:nth-child(83)",
    "#Content > p:nth-child(84)",
    "#Content > p:nth-child(86)",
    "#Content > p:nth-child(87)"
]

# Directory to save the output file
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Output file path
output_file = os.path.join(output_dir, "ai_for_ecommerce.txt")

with open(output_file, "w") as file:
    for css_selector in elements_to_scrape:
        element = soup.select_one(css_selector)
        if element:
            file.write(element.get_text() + '\n')
        else:
            file.write("element not found")

print(f" Text file saved in '{output_file}'")
