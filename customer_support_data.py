import requests
from bs4 import BeautifulSoup
import os

url = "https://www.helpscout.com/helpu/definition-of-customer-support/"

response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# List of CSS selectors
selectors = [
    "#gatsby-focus-wrapper > main > article > header > div > div > div.column.column--2-12-M.column--3-11-L > h1",
    "#Content > p:nth-child(1)",
    "#Content > p:nth-child(2)",
    "#Content > p:nth-child(3)",
    "#Content > p:nth-child(5)",
    "#Content > p:nth-child(7)",
    "#Content > p:nth-child(8)",
    "#Content > p:nth-child(9)",
    "#Content > p:nth-child(10)",
    "#Content > p:nth-child(11)",
    "#Content > p:nth-child(12)",
    "#Content > p:nth-child(15)",
    "#Content > p:nth-child(16)",
    "#Content > p:nth-child(17)",
    "#Content > section.ContentBlocks__ContentSECTION-sc-of5p5t-0.XneYp.ContentBlock.ContentBlockTable > div > div > table",
    "#Content > p:nth-child(19)",
    "#Content > p:nth-child(22)",
    "#Content > p:nth-child(23)",
    "#Content > p:nth-child(24)",
    "#Content > p:nth-child(25)",
    "#Content > p:nth-child(26)",
    "#Content > p:nth-child(29)",
    "#Content > h3:nth-child(30)",
    "#Content > p:nth-child(31)",
    "#Content > p:nth-child(32)",
    "#Content > p:nth-child(33)",
    "#Content > h3:nth-child(35)",
    "#Content > p:nth-child(36)",
    "#Content > p:nth-child(37)",
    "#Content > p:nth-child(38)",
    "#Content > h3:nth-child(40)",
    "#Content > p:nth-child(41)",
    "#Content > p:nth-child(42)",
    "#Content > p:nth-child(43)",
    "#Content > h3:nth-child(45)",
    "#Content > p:nth-child(46)",
    "#Content > p:nth-child(47)",
    "#Content > p:nth-child(48)",
    "#Content > p:nth-child(49)",
    "#Content > h3:nth-child(50)",
    "#Content > p:nth-child(51)",
    "#Content > p:nth-child(52)",
    "#Content > p:nth-child(53)",
    "#Content > p:nth-child(54)",
    "#Content > h3:nth-child(55)",
    "#Content > p:nth-child(56)",
    "#Content > p:nth-child(58)",
    "#Content > p:nth-child(59)",
    "#Content > h3:nth-child(61)",
    "#Content > p:nth-child(62)",
    "#Content > p:nth-child(63)",
    "#Content > p:nth-child(64)",
    "#Content > p:nth-child(65)",
    "#Content > h3:nth-child(67)",
    "#Content > p:nth-child(68)",
    "#Content > p:nth-child(69)",
    "#Content > p:nth-child(70)",
    "#Content > p:nth-child(73)",
    "#Content > p:nth-child(74)",
    "#Content > p:nth-child(75)",
    "#Content > p:nth-child(76)",
    "#gatsby-focus-wrapper > main > article > div > div > div.AuthorBylinestyles__AuthorBylineDIV-sc-1tcllg7-0.vuLZt.AuthorByline > div > h5 > a",
    "#gatsby-focus-wrapper > main > article > div > div > div.AuthorBylinestyles__AuthorBylineDIV-sc-1tcllg7-0.vuLZt.AuthorByline > div > div > p:nth-child(1)",
    "#gatsby-focus-wrapper > main > article > div > div > div.AuthorBylinestyles__AuthorBylineDIV-sc-1tcllg7-0.vuLZt.AuthorByline > div > div > p:nth-child(2)",
    "#gatsby-focus-wrapper > main > section.Section-sc-23pzt-0.PostsLandingstyles__PostsLandingMostRecentSECTION-sc-z2a5ju-0.hGnrPn.hAxSIg > div > div > div.grid > a.Cardstyles__CardLINK-sc-i1zpes-1.jqoYRR.Card.column.column--1-9-L.variant--FEATURED > article > header > h4",
    "#gatsby-focus-wrapper > main > section.Hero__HeroSECTION-sc-1kozof5-0.hSuEXO.Hero > div > div > div > h1",
    "#gatsby-focus-wrapper > main > section.Hero__HeroSECTION-sc-1kozof5-0.hSuEXO.Hero > div > div > div > p",
]

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "customer_support_data.txt")

with open(output_file, "w") as file:
    for css_selector in selectors:
        element = soup.select_one(css_selector)
        if element:
            file.write(element.get_text() + '\n')
        else:
            file.write("element not found")

print(f" Text file saved in '{output_file}'")
