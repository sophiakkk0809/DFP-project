import target_scraping as target
import Aldi_Scraping as aldi
import TJ_Scraping as tj
import csv
import sys

# call preloaded data by default
target_dict = target.load_data('support_files/preloaded_target.csv')
aldi_dict = aldi.load_data()
tj_dict = tj.load_data()


def refresh_data():
    """
    Asks each store scraping script to scrape fresh information from each website and updates the dictionaries.
    """
    global target_dict, aldi_dict, tj_dict

    target_dict = target.scrape_data()
    aldi_dict = aldi.scrape_data()
    tj_dict = tj.scrape_data()


def _search_store(prod_dict, keyword):
    """
    Finds and returns the cheapest product with the given keyword within the given dictionary of products.
    """
    min = (sys.float_info.max,)

    # loops thru each dictionary item for each store
    for product in prod_dict.items():
        # format for product = (product name, (category, price, quantity))
        if keyword.lower() in product[0].lower():
            # strip the $ at the beginning of the price
            price = float(product[1][1][1:])
            if price < min[0]:
                # min = (price as a float, (product name, category, price as a string, quantity))
                min = (price, (product[0], product[1][0], product[1][1], product[1][2]))

    # return the cheapest product as ((price as a float, (product name, category, price as a string, quantity)) for this store
    return min


def _find_cheapest(keyword):
    """
    Finds the cheapest product with the given keyword from the three stores.
    """
    # get the cheapest product for each store
    target_min = _search_store(target_dict, keyword)
    aldi_min = _search_store(aldi_dict, keyword)
    tj_min = _search_store(tj_dict, keyword)

    # find the cheapest product among the three stores
    min = target_min
    min_name = 'Target'

    if aldi_min[0] < min[0]:
        min = aldi_min
        min_name = 'Aldi'

    if tj_min[0] < min[0]:
        min = tj_min
        min_name = 'Trader Joes'

    if len(min)>1:
        # return cheapest product as (store name, (product name, category, price as string, quantity))
        return (min_name, min[1])
    else:
        return ('unable to find "'+keyword+'" in the groceries')

#TODO: implement getting the distance to a store
""" def find_distance(store_name):
    return (dist, time) """


def find_cheapest_product(keyword):
    """
    Orchestrates the process of finding the cheapest product with the matching keyword from the three stores and interfaces with the view
    """
    # get cheapest product in the format of (store name, (product name, category, price, quantity))
    prod = _find_cheapest(keyword)
    
    #TODO: call the distance function with the store that offers the cheapest product
    # distance = find_dist(prod[0])

    #TODO: interface with the view - displaying the below information
    # display, prod[0]<string name of store>, and prod[1]<tup = (product name, category, price, quantity)> on the view


def get_all_cat():
    all_cat=set([i[0] for i in target_dict.values()]+[i[0] for i in tj_dict.values()]+[i[0] for i in aldi_dict.values()])
    cw = csv.writer(open("cat_list.csv",'w'))
    cw.writerow(list(all_cat))


print(_find_cheapest('milk'))
# get_all_cat()
