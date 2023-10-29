import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_amazon(query, num_scrolls=10, wait_time=1):
    # Set the user-agent to mimic a real browser
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    # Create a Chrome WebDriver instance
    options = webdriver.ChromeOptions()

    # Set the user-agent
    options.add_argument(f'user-agent={USER_AGENT}')

    driver = webdriver.Chrome(options=options)

    try:
        # Build the Amazon search URL
        amazon_search_url = f"https://www.amazon.in/s?k={query}"

        # Navigate to the Amazon search page
        driver.get(amazon_search_url)

        # Scroll down to load more results
        for _ in range(num_scrolls):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(wait_time)
            except Exception as e:
                print(f"Error while scrolling: {str(e)}")

        # Extract the product information
        product_list = []

        # Use WebDriverWait to ensure the page has loaded completely
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.s-main-slot')))

        # Find the parent element containing the search results
        parent_element = driver.find_element(By.CSS_SELECTOR, '.s-main-slot')

        # Find all product elements within the parent element
        product_elements = parent_element.find_elements(By.CSS_SELECTOR, '.s-result-item')

        for product_element in product_elements:
            try:
                product_title = product_element.find_element(By.CSS_SELECTOR, '.a-size-medium, .a-text-normal').text
                product_price = product_element.find_element(By.CSS_SELECTOR, '.a-price, .a-offscreen').text
                product_rating = product_element.find_element(By.CSS_SELECTOR, '.a-icon-star-small').get_attribute('innerHTML')
                product_image_url = product_element.find_element(By.CSS_SELECTOR, '.s-image').get_attribute('src')

                # Add the product information to the list
                product_list.append({
                    'title': product_title,
                    'price': product_price,
                    'rating': product_rating,
                    'image_url': product_image_url
                })
            except NoSuchElementException:
                continue

        return product_list

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    product_name_or_category = input("Enter a product name or category: ")
    results = scrape_amazon(product_name_or_category)

    for product in results:
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"Rating: {product['rating']}")
        print(f"Image URL: {product['image_url']}")
        print()
