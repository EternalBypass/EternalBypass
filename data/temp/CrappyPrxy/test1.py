from bs4 import BeautifulSoup
import requests
r = requests.get('http://discord.com')
html_doc = r.content

soup = BeautifulSoup(html_doc, 'html.parser')

for link in soup.find_all('img'):
    print(link.get('src'))

#print(html_doc)