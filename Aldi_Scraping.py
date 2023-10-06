# import Selenium module & other modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from html import unescape
import time
import re
import pandas as pd
import csv


def get_pages_and_product_count(driver):
    WebDriverWait(driver, 10, poll_frequency=0.5, ignored_exceptions=None)
    product_count = driver.find_element(By.XPATH,"//div[contains(@class, 'product-listing-viewer__headline')]//span[@class='base-heading__post']").text
    #product_count = driver.find_element(By.XPATH, "//div[contains(@class, 'base-heading base-heading--h2 product-listing-viewer__headline')]//span[@class='base-heading__post']").text
    if product_count!='': product_count=int(re.sub(r'[^\d]+', '', product_count))
    
    if product_count>24:
        a = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//a[@class='base-pagination__count']")))]
        max_page = int(a[-1].strip())
    else: max_page=1

    return max_page ,product_count

def scrape_from_web():
    # open ALDI website
    options = Options()
    options.page_load_strategy = 'normal'
    #options.add_experimental_option("detach", True)
    #options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.get("https://new.aldi.us/")

    #driver.implicitly_wait(3) 
    #object of ActionChains
    a = ActionChains(driver)
    driver.set_window_size(880, 1080)


    # get all the Categories & Subcategory name
    driver.get("https://new.aldi.us/")
    driver.find_element(By.CLASS_NAME, "base-page-header__burger-icon").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'linklist-item flyout-submenu__item linklist-item--standard')]//*[contains(.,'Products')]/.."))).click()

    Cat_subcat_list = []
    Cat_subcat_url_list = []
    Cat = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='base-bordered-list__content']//span[@class='linklist-item__text']")))]
    Cat_name = [unescape(i).strip() for i in Cat]
    Cat_url = ['-'.join(unescape(i).strip().replace('&', '').lower().split()) for i in Cat]
    Cat_dict = {Cat_name[i]:Cat_url[i] for i in range(len(Cat_name))}

    for cat_name,cat_url in Cat_dict.items():
        xpath_subcat = "//button[contains(@class, 'linklist-item flyout-submenu__item linklist-item--standard')]//*[contains(.,'"+cat_name+"')]/.."
        button = driver.find_element(By.XPATH,xpath_subcat)
        button.click()
        Subcat = [my_elem.text for my_elem in driver.find_elements(By.XPATH, "//div[@class='base-bordered-list__content']//div[@class='linklist-item__text']") if my_elem.text!='']
        Subcat_url = ['-'.join(i.replace('&', '').replace(',','').lower().split()) for i in Subcat]
        Subcat_dict = {Subcat[i]:Subcat_url[i] for i in range(len(Subcat))}
        Cat_subcat_list.append({cat_name:Subcat})
        Cat_subcat_url_list.append({cat_url:Subcat_url})
        driver.find_element(By.XPATH, "//div[@class='base-flyout__sub-navi-headline']//span[@class='base-icon color--black']").click()


    driver.find_element(By.XPATH, "//button[contains(@class, 'base-flyout__close')]").click()


    #### MAIN (WIP)
    # Go to each Category
    Main_Page = "https://new.aldi.us/"
    Product_Page = "https://new.aldi.us/products/"
    driver.get(Main_Page)
    cnt = 0
    Cat_dict = dict()
    for cat in Cat_subcat_url_list:
        cnt+=1
        #(tryyy)# if cnt<14: continue
        cat_key,subcat_value = list(cat.items())[0]
        driver.get(Product_Page+cat_key)
        Subcat_list = []
        
        for subcat in subcat_value:
            ### if subcat=='milk-milk-substitutes' or subcat=='eggs' : continue
            ### Navigate to Subcategory product page
            driver.get(Product_Page+cat_key+'/'+subcat)
            time.sleep(2)
            
            ### Get Subcategory product cnt and max page
            max_page, product_count = get_pages_and_product_count(driver)
            print(subcat,max_page,product_count)
            time.sleep(1)
            
            ### Create list to store item info
            item_subcategory=[]
            item_names=[]
            item_brand_names=[]
            item_proportions=[]
            item_prices=[]
            item_details=[]

            ### Iterate between each page and products on page
            for i in range(1,max_page+1): 
                ### (tryyyy) ### if i<=5: continue
                # wait for website to load
                WebDriverWait(driver, 10, poll_frequency=0.5, ignored_exceptions=None)
                driver.get(Product_Page+cat_key+'/'+subcat)
                # when not in page 1, need to click to navigate to the page
                if i!=1 and i<=5:
                    xpath = "//div[@class='product-listing-viewer__pagination']//a[contains(@aria-label,'page "+ str(i) + "')]"
                    driver.find_element(By.XPATH,xpath).click()
                    WebDriverWait(driver, 30, poll_frequency=0.5, ignored_exceptions=None)
                # if pages>5 will not show at first page, need to navigate through clicking pages
                elif i>5:
                    for ii in range(5,i,2):
                        time.sleep(2)
                        xpath = "//div[@class='product-listing-viewer__pagination']//a[contains(@aria-label,'page "+ str(ii) + "')]"
                        driver.find_element(By.XPATH,xpath).click()
                        WebDriverWait(driver, 30, poll_frequency=0.5, ignored_exceptions=None)
                    time.sleep(3)
                    xpath = "//div[@class='product-listing-viewer__pagination']//a[contains(@aria-label,'page "+ str(i) + "')]"
                    driver.find_element(By.XPATH,xpath).click()
                    WebDriverWait(driver, 30, poll_frequency=0.5, ignored_exceptions=None)
                        
                time.sleep(3)   
                # count element on page to iterate over products on page
                element_cnt = len(driver.find_elements(By.XPATH, "//div[contains(@class, 'product-teaser-item product-grid__item')]"))
                print(element_cnt)


                brand_lst = driver.find_elements(By.XPATH,"//div[@class='product-grid']//div[contains(@class,'brandname')]")
                name_list = driver.find_elements(By.XPATH,"//div[@class='product-grid']//div[contains(@class,'tile__name')]")
                price_list = driver.find_elements(By.XPATH,"//div[@class='product-grid']//span[contains(@class,'base-price__regular')]")
                
                for i in range(element_cnt):
                    item_subcategory.append(subcat)
                    item_brand_names.append(brand_lst[i].text)
                    item_names.append(name_list[i].text)
                    item_prices.append(price_list[i].text)
                    

            ## Create Pandas table for each subcategory 
            lst = list(zip(item_subcategory,item_names,item_brand_names,item_prices))
            #print(lst)
            Subcat_list.append(pd.DataFrame(lst, columns =['Subcategory','Product Name', 'Brand', 'price'], dtype = float))
            # file_path=cat_key+'_'+subcat+'.csv'
            # #print(file_path)
            # pd.DataFrame(lst, columns =['Subcategory','Product Name', 'Brand', 'price'], dtype = float).to_csv(file_path)
        
        Cat_dict[cat_key]=Subcat_list
        time.sleep(1)
        
    all_df = pd.DataFrame()

    for k,v in Cat_dict.items():
        for subcat_df in v:
            subcat_df['Category']=k
            all_df = pd.concat([all_df,subcat_df],ignore_index=True)

    return all_df


def scrape_to_csv():
    all_df = scrape_from_web()
    all_df.to_csv('ALL_DF.csv')


def load_data():
    output_dict={}
    df = pd.read_csv('ALL_DF.csv')
    for i in df.iterrows():
        # print(i)
        # print(type(i))
        output_dict[i[1]['Product Name']] = (i[1]['Category'],i[1]['price'][1::],None)

    return output_dict

# Check if the script is run directly
if __name__ == "__main__":
    load_data()