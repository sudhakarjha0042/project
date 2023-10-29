import requests
from bs4 import BeautifulSoup

class Product:
    def __init__(self, title, price, img, url):
        self.title = title
        self.price = price
        self.img = img
        self.url = url

def scrape(query):
    snapdeal_url = "https://www.snapdeal.com/search"
    snapdeal_params = {"keyword": query}
    snapdeal_response = requests.get(snapdeal_url, params=snapdeal_params)
    snapdeal_soup = BeautifulSoup(snapdeal_response.content, 'html.parser')
    snapdeal_products = snapdeal_soup.find_all('div', class_='product-tuple-listing')

    flipkart_url = "https://www.flipkart.com/search"
    flipkart_params = {"q": query}
    flipkart_response = requests.get(flipkart_url, params=flipkart_params)
    flipkart_soup = BeautifulSoup(flipkart_response.content, 'html.parser')
    flipkart_products = flipkart_soup.find_all('div', class_='_1AtVbE')

    results = []

    for product in snapdeal_products:
        title = product.find('p', class_='product-title')
        price = product.find('span', class_='product-price')
        img = product.find('img', class_='product-image')

        if title and price and img:
            img_url = img.get('src') if img.get('src') else img.get('data-src')
            results.append(Product(title.text, price.text, img_url, "Snapdeal"))

    for product in flipkart_products:
        title = product.find('a', class_='IRpwTa')
        price = product.find('div', class_='_30jeq3')
        img = product.find('img', class_='_396cs4')

        if title and price and img:
            results.append(Product(title.text, price.text, img['src'], "Flipkart"))

    return results

# Example usage:
search_query = "laptop"
products = scrape(search_query)
for product in products:
    print(f"Title: {product.title}")
    print(f"Price: {product.price}")
    print(f"Image URL: {product.img}")
    print(f"Source: {product.url}")
    print()
