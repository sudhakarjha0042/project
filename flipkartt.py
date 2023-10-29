import requests
from bs4 import BeautifulSoup

def scrape_flipkart_products(search_query):
    # URL for Flipkart search results
    url = f"https://www.flipkart.com/search?q={search_query}"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the search results page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find product listings in the search results
        product_listings = soup.find_all('div', {'class': '_1AtVbE'})

        if not product_listings:
            print("No products found for the search query:", search_query)
            return

        # Loop through each product listing and print the details
        for product in product_listings:
            product_title = product.find('a', {'class': 's1Q9rs'}).text.strip()
            product_price = product.find('div', {'class': '_30jeq3'}).text.strip()
            product_rating = product.find('div', {'class': '_3LWZlK'}).text.strip()
            product_reviews = product.find('span', {'class': '_2_R_DZ'}).text.strip()

            print("Product Title:", product_title)
            print("Product Price:", product_price)
            print("Product Rating:", product_rating)
            print("Product Reviews:", product_reviews)
            print("")

    else:
        print("Failed to retrieve the search results. Status code:", response.status_code)

# Input for search query
search_query = input("Enter a product name or category to search on Flipkart: ")

# Call the function to scrape and display product details
scrape_flipkart_products(search_query)
