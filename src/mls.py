#C:\Python27\python scrape.py

from bs4 import BeautifulSoup
import requests

source = requests.get("http://coreyms.com").text

soup = BeautifulSoup(source, "html.parser")

print(soup.prettify())

