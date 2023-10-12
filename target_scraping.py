from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict


def _get_categories_link(driver: webdriver.Chrome) -> list:
    """
    This class returns a list of paths to the different categories in target
    """
    path = "https://www.target.com/c/shop-all-categories/-/N-5xsxf?prehydrateClick=true"
    driver.get(path)
    # wait for categories to exist
    categories = WebDriverWait(driver,50).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="pageBodyContainer"]/div/div[1]/div/div[14]'))
            )
    # get the categories list
    categories_ls = categories.find_elements(By.CLASS_NAME, "cQxfob")
    links = []
    for category in categories_ls[1::]:
        cat = category.find_elements(By.TAG_NAME, 'a')
        links.append(cat[0].get_attribute('href'))

    return links


def _get_subcategories_link(link: str, driver: webdriver.Chrome) -> list:
    """
    This class returns a list of paths to the different sub Grocery categories in target
    """
    driver.get(link)
    subs = WebDriverWait(driver,50).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jUzyfh"))
            )
    subs_list = subs.find_elements(By.TAG_NAME, 'li')

    href_subcat = []
    for item in subs_list:
        h = item.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
        sub_cat = item.find_elements(By.TAG_NAME, 'span')
        href_subcat.append((h, sub_cat[0].text))
    return href_subcat


def _get_data_with_path(path: str, sub_category: str, driver: webdriver.Chrome):
    """
    this function returns a dictionary with product data for the path give
    with the form { product_name: (category, price, quantity)  }
    """
    if ',' in sub_category:
        sub_category = sub_category.split(",")
        sub_category = sub_category[0]

    driver.get(path)

    data = defaultdict(list)

    try:
        main = WebDriverWait(driver,50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kmNUvV"))
        )

        articles = main.find_elements(By.CLASS_NAME, "dOpyUp")

        for article in articles:
            art = [sub_category]
            title = article.find_elements(By.CLASS_NAME, "iZqUcy")
            if not title:
                continue
            else:
                # art.append(title[0].text.strip())
                t = title[0].text.strip()

            # find price
            price = article.find_elements(By.CLASS_NAME, "kKRufV")
            price = price[0].text
            idx = price.find("$")

            end = -1
            for j, letter in enumerate(price[1:]):
                if not letter.isnumeric() and letter != ".":
                    end = j
                    break
            if end <= 0:
                continue

            price = price[1:end+1]

            try:
                art.append(float(price))
            except:
                print(f"Error: price'{price} cannot be converted to float'")
                print(price)
                continue

            art.append(0)
            data[t] = tuple(art)

    finally:
        return data


def write_to_file(data: dict, path: str):
    """
    this functions writes a dictionary data to the given path
    """
    f = open(path, 'w')

    # 'product name' :(category, price, quantity)
    f.write('name, category, price, quantity\n')
    for key, item in data.items():
        key = key.replace(",", "")
        f.write(key + "," + str(item[0]) + "," + str(item[1]) + "," + str(item[2]) + "\n")

    f.close()


def load_data(path: str) -> dict:
    """
    This function takes a path as parameter and returns a dictionary of tuples with the form
    {name: (category, price, quantity)} filled with the data of the csv
    """
    file = open(path, 'r',encoding = 'latin1')
    data = {}
    i = 0
    for line in file:
        if i == 0:
            i+=1
            continue
        else:
            name, category, price, quantity = line.strip().split(",")
            price, quantity = str(price), int(quantity)
            data[name] = (category, price, quantity)

    return data


def get_all_data() -> dict:
    """
    this function returns a dictionary of the form { name: (category, price, quantity) } with all the data from target
    """
    print("Target Scraping in progress. This will take a few minutes...")
    options = Options()
    options.page_load_strategy = 'normal'
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    categories_links = _get_categories_link(driver)
    links_subcat = []
    for link in categories_links:
        links_subcat.extend(_get_subcategories_link(link, driver))

    links_subcat = links_subcat[2::]
    all_data = {}
    for path, sub_category in links_subcat:
        all_data.update(_get_data_with_path(path, sub_category, driver))


    print("Finished Scraping")
    return all_data


def scrape_data():
    all_dict = get_all_data()
    write_to_file(all_dict,'support_files/preloaded_target.csv')

def main():
    all_dict = get_all_data()
    write_to_file(all_dict,'support_files/preloaded_target.csv')


if __name__ == "__main__":
    main()

# data = get_all_data()
# write_to_file(data,'preloaded_targetdata.csv')
# print(data)