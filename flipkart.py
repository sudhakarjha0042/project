import requests
from bs4 import BeautifulSoup

class Product:
    def __init__(self, title, price, img):
        self.title = title
        self.price = price
        self.img = img

def scrape_flipkart(query):
    url = f"https://www.flipkart.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_cards = soup.find_all('div', class_='_1AtVbE')

    results = []

    for product_card in product_cards:
        title = product_card.find('a', class_='IRpwTa')
        price = product_card.find('div', class_='_30jeq3')
        img = product_card.find('img', class_='_396cs4')

        if title and price and img:
            results.append(Product(title.text, price.text, img['src']))

    return results

# Example usage:
search_query = "laptop"
products = scrape_flipkart(search_query)
for product in products:
    print(f"Title: {product.title}")
    print(f"Price: {product.price}")
    print(f"Image URL: {product.img}")
    print()
