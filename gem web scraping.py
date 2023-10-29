import requests
from bs4 import BeautifulSoup

# Function to scrape product details from a product page
def scrape_product_details(product_url, category_name):
    print("Scraping product page:", product_url)
    product_response = requests.get(product_url)
    if product_response.status_code == 200:
        product_soup = BeautifulSoup(product_response.text, 'html.parser')

        # Find all product items on the page
        product_items = product_soup.find_all("li", class_="clearfix")

        for product in product_items:
            # Extract the product title and its URL
            product_title_element = product.find("span", class_="variant-title")
            if product_title_element:
                product_title = product_title_element.find("a")["title"]
                product_url = "https://mkp.gem.gov.in" + product_title_element.find("a")["href"]
            else:
                product_title = "Not available"
                product_url = "Not available"

            # Extract the seller information
            seller_info = product.find("div", class_="seller-info")
            if seller_info:
                seller_name_element = seller_info.find("span", class_="seller-info-caption")
                seller_resellers_element = seller_info.find("span", class_="sold_as_summary")
                if seller_name_element:
                    seller_name = seller_name_element.next_sibling.strip()
                else:
                    seller_name = "Not available"

                if seller_resellers_element:
                    seller_resellers = seller_resellers_element.text.strip()
                else:
                    seller_resellers = "Not available"
            else:
                seller_name = "Not available"
                seller_resellers = "Not available"

            # Extract seller rating (if available)
            seller_rating_element = product.find("div", class_="overall-rating")
            if seller_rating_element:
                seller_rating = seller_rating_element.text.strip()
            else:
                seller_rating = "Not available"

            # Extract the brand
            product_brand_element = product.find("div", class_="variant-brand")
            if product_brand_element:
                product_brand = product_brand_element.text.strip().replace("Brand:", "").strip()
            else:
                product_brand = "Not available"

            # Extract the minimum quantity per consignee (MOQ)
            moq_element = product.find("div", class_="variant-moq")
            if moq_element:
                moq = moq_element.text.strip().replace("Min. Qty. Per Consignee:", "").strip()
            else:
                moq = "Not available"

            # Extract the product prices
            list_price_element = product.find("span", class_="variant-list-price")
            final_price_element = product.find("span", class_="variant-final-price")
            if list_price_element and final_price_element:
                list_price = list_price_element.find("span", class_="m-w").text.strip()
                final_price = final_price_element.find("span", class_="m-w").text.strip()
            else:
                list_price = "Not available"
                final_price = "Not available"

            # Check if all product details are "Not available"
            if (
                product_title == "Not available" and
                product_url == "Not available" and
                seller_name == "Not available" and
                seller_resellers == "Not available" and
                seller_rating == "Not available" and
                product_brand == "Not available" and
                moq == "Not available" and
                list_price == "Not available" and
                final_price == "Not available"
            ):
                continue
            else:
                # Print the extracted information
                print(f"Category: {category_name}")
                print(f"Product Title: {product_title}")
                print(f"Product URL: {product_url}")
                print(f"Seller Name: {seller_name}")
                print(f"Seller Resellers: {seller_resellers}")
                print(f"Seller Rating: {seller_rating}")
                print(f"Product Brand: {product_brand}")
                print(f"Minimum Qty Per Consignee: {moq}")
                print(f"List Price: {list_price}")
                print(f"Final Price: {final_price}")
                print()

    else:
        print("Failed to retrieve product page. Status code:", product_response.status_code)

# Ask the user for the product name or category
product_name = input("Enter the product name or category: ")

# Construct the URL with the user's input
url = f"https://mkp.gem.gov.in/search?q={product_name}"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    category_list = soup.find("ul", class_="clearfix")

    if category_list:
        categories = category_list.find_all("li", class_="bn-group")

        for category in categories:
            category_name = category.find("strong").text.strip()
            category_links = category.find_all("a")

            print(f"Category: {category_name}")
            for link in category_links:
                link_text = link.text.strip()
                link_url = "https://mkp.gem.gov.in" + link["href"]
                print(f"  Link: {link_text}, URL: {link_url}")

                # Call the scrape_product_details function for each category link
                scrape_product_details(link_url, category_name)
    else:
        print("Category list not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)


# Ask the user for the product name or category
product_name = input("Enter the product name or category: ")

# Construct the URL with the user's input
url = f"https://mkp.gem.gov.in/search?q={product_name}"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    category_list = soup.find("ul", class_="clearfix")

    if category_list:
        categories = category_list.find_all("li", class_="bn-group")

        for category in categories:
            category_name = category.find("strong").text.strip()
            category_links = category.find_all("a")

            for link in category_links:
                link_text = link.text.strip()
                link_url = "https://mkp.gem.gov.in" + link["href"]

                # Call the scrape_product_details function for each category link
                scrape_product_details(link_url, category_name)
    else:
        print("Category list not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)