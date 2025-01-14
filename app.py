import requests
from bs4 import BeautifulSoup
import sqlite3

response = requests.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=iphon&_sacat=0")
soup = BeautifulSoup(response.text, 'html.parser')

products = soup.find_all("div", class_="s-item__info")
images = soup.find_all("div", class_="s-item__image-wrapper image-treatment")
links = soup.find_all("a", class_="s-item__link")

conn = sqlite3.connect('products.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products
             (name TEXT, price TEXT, img TEXT, link TEXT)''')

c.execute('''DELETE FROM products''')
conn.commit()

for product, img, link in zip(products, images, links):
    title = product.find("span", role="heading")
    price = product.find("span", class_="s-item__price")
    img_tag = img.find("img")
    link_tag = link.get('href')
    
    if title and price and img_tag and link_tag:
        print(f"name: {title.text}")
        print(f"price: {price.text}")
        print(f"image: {img_tag['src']}")
        print(f"link: {link_tag}")
        
        c.execute("INSERT INTO products (name, price, img, link) VALUES (?, ?, ?, ?)",
                  (title.text.strip(), price.text.strip(), img_tag['src'], link_tag))

conn.commit()
conn.close()
