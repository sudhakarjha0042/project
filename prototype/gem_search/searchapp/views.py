from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import SearchResult
from .forms import ProductSearchForm

def scrape_product_details(product_url):
    product_response = requests.get(product_url)
    if product_response.status_code == 200:
        product_soup = BeautifulSoup(product_response.text, 'html.parser')
        product_items = product_soup.find_all("li", class_="clearfix")
        product_details = []

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

            # Append the product details to the list
            product_details.append({
                "product_title": product_title,
                "product_url": product_url,
                "seller_name": seller_name,
                "seller_resellers": seller_resellers,
                "seller_rating": seller_rating,
                "product_brand": product_brand,
                "moq": moq,
                "list_price": list_price,
                "final_price": final_price
            })

        return product_details
    else:
        return []


def search(request):
    results = None

    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            url = f"https://mkp.gem.gov.in/search?q={product_name}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                category_list = soup.find("ul", class_="clearfix")

                if category_list:
                    categories = category_list.find_all("li", class_="bn-group")
                    results = []

                    for category in categories:
                        category_name = category.find("strong").text.strip()
                        category_links = category.find_all("a")

                        category_result = SearchResult()
                        category_result.category = category_name
                        category_result.links = []

                        for link in category_links:
                            link_text = link.text.strip()
                            link_url = "https://mkp.gem.gov.in" + link["href"]
                            category_result.links.append((link_text, link_url))

                            # Call the scrape_product_details function for each category link
                            product_details = scrape_product_details(link_url)
                            category_result.product_details = product_details

                        results.append(category_result)
                else:
                    error_message = "Category list not found on the page."
                    results = [error_message]  # Convert error message to a list
            else:
                error_message = "Failed to retrieve the webpage. Status code: " + str(response.status_code)
                results = [error_message]  # Convert error message to a list
    else:
        form = ProductSearchForm()

    return render(request, 'searchapp/search.html', {'form': form, 'results': results})
