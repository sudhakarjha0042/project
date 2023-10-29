import time
import requests
from bs4 import BeautifulSoup

# Function to send a request with retries
def send_request(url):
    retries = 3
    while retries > 0:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except (requests.RequestException, Exception) as e:
            print(f"Request failed: {str(e)}")
            retries -= 1
            time.sleep(5)  # Add a delay before retrying
    raise Exception("Max retries reached, request failed.")

# Function to scrape GEM
def scrape_gem(product_name):
    gem_url = f"https://mkp.gem.gov.in/search?q={product_name}"
    gem_response = send_request(gem_url)

    # Parse the HTML response using BeautifulSoup
    gem_soup = BeautifulSoup(gem_response.content, 'html.parser')

    # Find product elements on the GEM search page
    gem_product_elements = gem_soup.find_all('div', class_='search-list')

    # Create a list to store the product information from GEM
    gem_product_list = []

    for product_element in gem_product_elements:
        try:
            product_title = product_element.find('h2').text
            product_price = product_element.find('span', class_='price-box').text
            product_image_url = product_element.find('img').get('src')

            # Add the product information to the list
            gem_product_list.append({
                'title': product_title,
                'price': product_price,
                'image_url': product_image_url
            })
        except:
            continue

    print("GEM Products:")
    for product in gem_product_list:
        print(f"{product['title']} - {product['price']} - {product['image_url']}")

# Function to scrape Amazon
def scrape_amazon(product_name):
    amazon_url = f"https://www.amazon.in/s?k={product_name}"
    
    # Send a request to the Amazon search URL
    amazon_response = send_request(amazon_url)

    # Parse the HTML response using BeautifulSoup
    amazon_soup = BeautifulSoup(amazon_response.content, 'html.parser')

    # Find product elements on the Amazon search page
    amazon_product_elements = amazon_soup.find_all('div', class_='s-result-item s-asin')

    # Create a list to store the product information from Amazon
    amazon_product_list = []

    for product_element in amazon_product_elements:
        try:
            product_title = product_element.find('span', class_='a-text-normal').text
            product_price = product_element.find('span', class_='a-price').text
            product_image_url = product_element.find('img', class_='s-image').get('src')

            # Add the product information to the list
            amazon_product_list.append({
                'title': product_title,
                'price': product_price,
                'image_url': product_image_url
            })
        except:
            continue

    print("Amazon Products:")
    for product in amazon_product_list:
        print(f"{product['title']} - {product['price']} - {product['image_url']}")

# Main function
def main():
    product_name = input("Enter a product name or category: ")
    website_choice = input("Enter the website to search (Amazon/GEM): ").lower()

    if website_choice == "amazon":
        scrape_amazon(product_name)
    elif website_choice == "gem":
        scrape_gem(product_name)
    else:
        print("Invalid website choice. Please enter 'Amazon' or 'GEM'.")

if __name__ == "__main__":
    main()
