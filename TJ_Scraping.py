from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import csv

"""
This Python file scrapes product information from the food section from the Trader Joe's website. It outputs
the information in a .csv file called output.csv Functions beginning with '_' are private.

Alex Hewitson
"""

# Initialize an empty dictionary to store the product information
_prod_dict = {}


def _scrape_page(driver):
    """
    Puts the products in the TJs page into a dictionary in the format of product name: (category, price, quantity)
    """

    # get the list of products from the HTML
    prods_list_str = driver.find_element(By.CLASS_NAME, "ProductList_productList__list__3-dGs").text

    # split individual products into a list
    product_entries = prods_list_str.split("ADD TO LIST\n")

    # format each product's information and add to the dictionary
    for prod in product_entries:
        prod_details = prod.strip().split('\n')
        # dictionary format = product name: (category, price, quantity)
        _prod_dict[prod_details[1]] = (prod_details[0], prod_details[2].split('/')[0].replace("$", ""), prod_details[2].split('/')[1])


def _scrape_all_products(driver):
    """
    Logic for clicking the next page button and calling the scrape_page function when appropriate
    """

    next_button_selector = ".Pagination_pagination__arrow__3TJf0.Pagination_pagination__arrow_side_right__9YUGr"

    # loop through each page in the food category
    while True:
        try:
            # scroll to the next page button
            driver.execute_script("window.scrollTo(0, 3500);")
            
            # Wait for the next page button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_selector))
            )

            # scrape data from the current page
            _scrape_page(driver)

            # Use ActionChains to click the next button with a slight delay
            action = ActionChains(driver)
            action.move_to_element(next_button).pause(1).click().perform()

        except TimeoutException:
            # scrape the last page
            _scrape_page(driver)
            break

        except Exception as e:
            # handle errors
            print(f"Error: {e}")
            break


def scrape_data():
    """
    Orchestrates the process of scraping data from the Trader Joes website and returns the data in _prod_dict
    """

    _prod_dict.clear()
    # start the webpage
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)

    driver.set_window_size(880, 1080)
    driver.get("https://www.traderjoes.com/home/products/category/food-8")

    print("TJs Scraping in progress. This will take a few minutes...")
    # scrape the webpage
    _scrape_all_products(driver)
    driver.quit()

    print("Finished Scraping")

    return _prod_dict


def load_data():
    """
    Accepts a .csv file of preloaded product data (outputted from _write_file()) and converts it to a dictionary in _prod_dict
    """
    
    _prod_dict.clear()

    with open('support_files/preloaded_tj.csv', mode='r', newline='', encoding='ISO-8859-1') as file_input:
        reader = csv.DictReader(file_input)
        
        for row in reader:
            # Create a tuple containing category, price, and quantity
            product_data = (row['Category'], row['Price'], row['Quantity'])
            
            # Add the data to the dictionary with product_name as the key
            _prod_dict[row['Product Name']] = product_data
    
    return _prod_dict


def _write_file():
    """
    Expects the dictionary format to be product name: (category, price, quantity) then converts the dictionary to a .csv
    """

    # Open the CSV file for writing
    with open('output.csv', 'w', newline='') as file_output:
    # Create a CSV writer object
        csv_writer = csv.writer(file_output)
        
        # Write the header row
        csv_writer.writerow(['Product Name', 'Category', 'Price', 'Quantity'])
        
        # Write the data rows
        for product_name, product_info in _prod_dict.items():
            csv_writer.writerow([product_name, *product_info])


def main():
    # scrape new product data from the website
    scrape_data()

    # load existing product data from preloaded_tj.csv
    #load_data()

    # write the dictionary of products to an output .csv file
    _write_file()
    

# Check if the script is run directly
if __name__ == "__main__":
    main()