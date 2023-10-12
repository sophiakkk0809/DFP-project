from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import model as md
import Journey as loc
import datetime
root = Tk()

category_set = [
    "Milk",
    "Cheese",
    "Eggs",
    "Yogurt",
    "Chips",
    "Spreads",
    "Breads",
    "Beef",
    "Seafood",
    "Lamb",
    "Pasta",
    "Ice Cream",
    "Creamy",
    "Pork",
    "Chicken",
    "Nuts",
    "Baby",
    "Fruits",
    "Cereals",
    "Seasoning",
    "Salad",
    "Drink"
]


# format settings
padding = {'padx':15, 'pady':10} # set widgets space
padding_ls = {'padx':10, 'pady':7} # set widgets space

# SEPERATE FRAME
root.title("Save Mart")
root.geometry('1500x1500')
topframe = Frame(root)
topframe.pack(side= TOP)
optionframe = Frame(root)
optionframe.pack(side= TOP)
searchframe = Frame(root)
searchframe.pack(side= TOP)
resultframe = Frame(root)
resultframe.pack(side= TOP)

#Define a function to clear the content of the text widget
def click_clear_default(event, default_text):
    entry_widget = event.widget
    
    # Only clear the widget if it still contains the default text
    if entry_widget.get() == default_text:
        entry_widget.delete(0, 'end')
        entry_widget.configure(fg='black')  # Change text color to black when it is active
        entry_widget.unbind('<Button-1>')  # Unbind the event after it's clicked once to allow for text selection
  

# IMAGE
image_path = "support_files/healthyfood.jpg"
image = Image.open(image_path)
original_width, original_height = image.size
new_height = int(original_height * 0.6)
image = image.resize((original_width, new_height), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image, master=root)
# Topic
label1 = Label(topframe, text = 'Save Mart', font=('Futura', 32),relief='ridge', borderwidth=7, compound="top", image=photo)
label1.pack(**padding, fill=X)

# Refresh data
lf1 = LabelFrame(optionframe, text='Refresh Data', font=('Futura', 14))
lf1.pack(**padding, ipadx=200, ipady=60, anchor=NW, side=LEFT, fill=X)
lf1.pack_propagate(0)
# refresh button
refresh_btn = Button(lf1, text="Refresh data", borderwidth=3, relief="raised", font=('Futura', 16))
refresh_btn.pack(**padding, ipady=5, side = LEFT)

                                             
# Search
lf2 = LabelFrame(optionframe, text='Product', font=('Futura', 14))
lf2.pack(**padding, ipadx=200, ipady=60, anchor=NW, side=LEFT, fill=X)
lf2.pack_propagate(0)
# label
label2 = Label(lf2, text = 'Search for a product', font=('Futura', 18))
label2.pack(fill=X)
# Search for Category
search_cat_text = StringVar()
default_text_1 = 'Seach'
search_cat_entry = Entry(lf2, width = 20, fg='gray', font=('Futura', 15))
search_cat_entry.insert(0, default_text_1)
search_cat_entry.pack(**padding,fill=X)
clicked = search_cat_entry.bind('<Button-1>',lambda event : click_clear_default(event,default_text_1))
Searched_text = search_cat_text.get()

# #Location
# lf2= LabelFrame(optionframe, text='Location', font=('Futura', 14))
# lf2.pack(**padding, ipadx=150, ipady=13, anchor=NW, side=TOP, fill=X)
# #label
# label2 = Label(lf2, text = 'Select a location', font=('Futura', 18))
# label2.pack(fill=X)
# #option menu
# loc_value = StringVar(optionframe)
# loc_value.set("Select")
# location_str = set(location_list)
# loc_font = tkFont.Font(family='Futura',size=15)
# location_menu = OptionMenu(lf2, loc_value, *location_str)
# location_menu.config(font=loc_font)
# location_menu.pack(**padding, fill=X)
# Selected_loc = loc_value.get()



# Search for location
search = Label(searchframe, text="Search Location", font=('Futura', 18))
search.pack(fill=X)
search_text = StringVar()
default_text_2 = "Type in your address, format: 4800,Forbes,Ave,Pittsburg,PA,15213 "
search_entry = Entry(searchframe, width = 50, fg='gray', font=('Futura', 15))
search_entry.insert(0, default_text_2)
search_entry.pack(**padding, ipadx = 60, ipady = 10, side=LEFT)
clicked = search_entry.bind('<Button-1>',lambda event : click_clear_default(event,default_text_2))
Selected_loc = search_text.get()
# SEARCH button
search_btn = Button(searchframe, text="Search", borderwidth=3, relief="raised", font=('Futura', 20))
search_btn.pack(**padding, ipady=5, side = LEFT)
# CLEAR button
clear_btn = Button(searchframe, text="Clear", borderwidth=3, relief="raised", font=('Futura', 20))
clear_btn.pack(ipady=5, side = LEFT)

# Selected_cat - chosen category
# Selected_loc - input address


def refresh_data():
    try:
        md.refresh_data()
        current_time = datetime.datetime.now()
        refreshed = Label(lf1, text = 'Latest data downloaded at : \n'+ current_time.strftime("%Y-%m-%d %H:%M:%S") , font=('Futura', 15))
        refreshed.pack(**padding, fill=X) 
    except:
        current_time = datetime.datetime.now()
        refreshed = Label(lf1, text = 'Unable to refreshed data, Please close and open the app again' , font=('Futura', 14), wraplength=200)
        refreshed.pack(**padding, fill=X) 
    
    


def get_product(keyword):
    try:
        cheapest = md._find_cheapest(keyword)
    except:
        cheapest = ('error',('error','error','0','0'))
    ### if not find need to output something instead than have error 
    # .........
    ###
    return cheapest
    # (store name, (product name, category, price as string, quantity))


def get_location(Selected_loc): # input the user address

    target = loc.get_shortest_journey(Selected_loc, 'Target')
    aldi = loc.get_shortest_journey(Selected_loc, 'Aldi')
    tj = loc.get_shortest_journey(Selected_loc, 'Trader Joes')

    loc_result = {'aldi':aldi,'tj':tj,'target':target}
    return loc_result 
    # (3.4 miles(str), 10min (str))


# return two dictionary 
#   1. result min price product 
#   2. tuple of location
result_canvas = Canvas(resultframe, height=100, width=100)

def build_canvas():
    # RESULT
    #result_scrollbar = Scrollbar(resultframe, orient="horizontal", command=result_canvas.xview)
    result_canvas.config(scrollregion=(0,0,3000,700))#, xscrollcommand=result_scrollbar.set)

    #result_scrollbar.pack(side=BOTTOM, fill=X)
    result_canvas.pack(ipadx=500, ipady=170, fill=BOTH)

    resultframe1 = Frame(resultframe)
    result_canvas.create_window(570,180,window=resultframe1)

    return result_canvas,resultframe1

def clear_canvas():
    result_canvas.delete(ALL)
    print('cleared')


def show_results():
    result_canvas,resultframe1 = build_canvas()
    Searched_text = search_cat_entry.get()
    Selected_loc = search_entry.get()
    print(Searched_text,Selected_loc)
    # all_result = get_product(Selected_cat.lower())
    # all_result = ('Aldi', ('2% Milk Reduced Fat American Cheese Singles, 16 count', 'dairy-eggs', '2.09', None))
    all_location = get_location(Selected_loc)
    all_result = get_product(Searched_text.lower())

    result= LabelFrame(resultframe1)
    result.pack(**padding, ipadx=190,ipady=170, side=TOP)
    result.pack_propagate(0)

    if (type(all_result)==str):
        cat_label = Label(result, text = all_result, font=('Futura', 18), wraplength=300)
        cat_label.pack(**padding, ipady=50)
    
    else:
        for i in range(1):
            #output type
            #all_result = {'almond milk':('milk','$4',3), 'aldi eggs':('milk','$1.99',5), 'rib eye':('meat','$17.39',2), 'ice cream':('Frozen','$5.90',61)}
            shop = all_result[0]
            Cat = all_result[1][1]
            product = all_result[1][0]
            price = all_result[1][2]
            if len(product.split()) >= 10 :
                product_label = Label(result, text = product , font=('Futura', 22), wraplength=320)
                product_label.pack(**padding_ls, ipady=10)
            else :
                product_label = Label(result, text = product , font=('Futura', 25), wraplength=320)
                product_label.pack(**padding_ls, ipady=10)
            cat_label = Label(result, text = 'Category : '+Cat , font=('Futura', 20))
            cat_label.pack(ipady=10)
            price_label = Label(result, text = "Price : $ "+price , font=('Futura', 17))
            price_label.pack(**padding_ls, ipady=5)
            shop_label = Label(result, text = "Shop : "+all_location['aldi'][2] , font=('Futura', 17))
            shop_label.pack(ipady=5)
            if(shop=='Aldi'):
                price_label = Label(result, text = "Location : "+str(all_location['aldi'][0:2]), font=('Futura', 17))
                price_label.pack(**padding_ls, ipady=5)
            elif(shop=='Target'):
                price_label = Label(result, text = "Location : "+str(all_location['target'][0:2]) , font=('Futura', 17))
                price_label.pack(**padding_ls, ipady=5)
            else:
                price_label = Label(result, text = "Location : "+str(all_location['tj'][0:2]) , font=('Futura', 17))
                price_label.pack(**padding_ls, ipady=5)

    return result_canvas


search_btn.config(command=show_results)
clear_btn.config(command=clear_canvas)
refresh_btn.config(command=refresh_data)

root.mainloop()