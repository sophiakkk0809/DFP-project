from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
root = Tk()

#input type
aldi_dict = {'almond milk':('diaries','$4',3), 'aldi eggs':('diaries','$1.99',5), 'rib eye':('meat','$17.39',2), 'ice cream':('Frozen','$5.90',61)}
tj_dict = {'oatmilk':('milk and eggs','$4.53',3), 'TJeggs':('milk and eggs','$2.34',5), 'rib eye premium':('meat','$31.39',2), 'Hagendaze':('Desert','$43.30',61)}
category_set = []
for i,j in aldi_dict.items():
    category_set.append(j[0])
location_list = ['Shadyside','squirrel hill']

#output type
all_result = {'almondss milk':('milk','$4',3), 'aldiss eggs':('milk','$1.99',5),'almsond milk':('milk','$4',3), 'aldssi eggs':('milk','$1.99',5),'almond milk':('milk','$4',3), 'aldi eggs':('milk','$1.99',5), 'rib eye':('meat','$17.39',2), 'ice cream':('Frozen','$5.90',61),'oat milk':('milk','$4',3), 'eggs':('milk','$1.99',5), 'rib eye premium':('meat','$17.39',2), 'ch ice cream':('Frozen','$5.90',61),'almond milkss':('milk','$4',3), 'aldi eggsss':('milk','$1.99',5), 'rib eyess':('meat','$17.39',2), 'ice creamss':('Frozen','$5.90',61)}

# format settings
padding = {'padx':15, 'pady':10} # set widgets space

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


#IMAGE
image_path = "/Users/sophiakuo/Documents/23F-Python/Project/Code/healthyfood.jpg"
image = Image.open(image_path)
original_width, original_height = image.size
new_height = int(original_height * 0.6)
image = image.resize((original_width, new_height), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image, master=root)
#Topic
label1 = Label(topframe, text = 'Save Mart', font=('Futura', 32),relief='ridge', borderwidth=7, compound="top", image=photo)
label1.pack(**padding, fill=X)

#Category
lf1 = LabelFrame(optionframe, text='Category', font=('Futura', 14))
lf1.pack(**padding, ipadx=80, ipady=13, anchor=NW, side=LEFT, fill=X)
#label
label2 = Label(lf1, text = 'Select a category', font=('Futura', 18))
label2.pack(fill=X)
#option menu
cat_value = StringVar(optionframe)
cat_value.set("Select")
Category_str = set(category_set)
cat_font = tkFont.Font(family='Futura',size=15)
category_menu = OptionMenu(lf1, cat_value, *Category_str)
category_menu.config(font=cat_font)
category_menu.pack(**padding, fill=X)
Selected_cat = cat_value.get()

#Location
lf2= LabelFrame(optionframe, text='Location', font=('Futura', 14))
lf2.pack(**padding, ipadx=150, ipady=13, anchor=NW, side=TOP, fill=X)
#label
label2 = Label(lf2, text = 'Select a location', font=('Futura', 18))
label2.pack(fill=X)
#option menu
loc_value = StringVar(optionframe)
loc_value.set("Select")
location_str = set(location_list)
loc_font = tkFont.Font(family='Futura',size=15)
location_menu = OptionMenu(lf2, loc_value, *location_str)
location_menu.config(font=loc_font)
location_menu.pack(**padding, fill=X)
Selected_loc = loc_value.get()


#Define a function to clear the content of the text widget
def click_clear_default(event):
   search_entry.configure(state=NORMAL)
   search_entry.delete(0, END)
   search_entry.unbind('<Button-1>', clicked)
# searchbox
search = Label(searchframe, text="Search Product", font=('Futura', 18))
search.pack(fill=X)
search_text = StringVar()
search_entry = Entry(searchframe,textvariable = search_text, width = 50, fg='gray', font=('Futura', 15))
search_entry.insert(0, "Search by product name/ brand/ product category")
search_entry.pack(**padding, ipadx = 100, ipady = 10, side=LEFT)
clicked = search_entry.bind('<Button-1>', click_clear_default)
Searched = search_text.get()
# SEARCH
search_btn = Button(searchframe, text="Search", borderwidth=3, relief="raised", font=('Futura', 20))
search_btn.pack(**padding, ipady=5)

# Selected_cat
# Selected_loc
# Searched


## Generate a result list by searched word and selected_cat & location
def find_product():
    print(all_result)

# RESULT
result_canvas = Canvas(resultframe, height=100, width=100)

result_scrollbar = Scrollbar(resultframe, orient="horizontal", command=result_canvas.xview)
result_canvas.config(scrollregion=(0,0,3000,700), xscrollcommand=result_scrollbar.set)

result_scrollbar.pack(side=BOTTOM, fill=X)
result_canvas.pack(ipadx=450, ipady=200, fill=BOTH)

resultframe1 = Frame(resultframe)
result_canvas.create_window(450,160,window=resultframe1)

def show_results():
    for i,v in all_result.items():
        #output type
        #all_result = {'almond milk':('milk','$4',3), 'aldi eggs':('milk','$1.99',5), 'rib eye':('meat','$17.39',2), 'ice cream':('Frozen','$5.90',61)}
        Cat = i
        product = v[0]
        price = v[1]
        quantity = v[2]
        result= LabelFrame(resultframe1)
        result.pack(**padding, ipadx=100,ipady=150, side=LEFT, fill=Y)
        result.pack_propagate(0)
        cat_label = Label(result, text = product , font=('Futura', 18))
        cat_label.pack(**padding, ipady=10)
        product_label = Label(result, text = Cat , font=('Futura', 20))
        product_label.pack(**padding, ipady=10)
        price_label = Label(result, text = "Price : "+price , font=('Futura', 15))
        price_label.pack(**padding, ipady=5)
        quantity_label = Label(result, text ="Quantity : "+str(quantity) , font=('Futura', 15))
        quantity_label.pack(**padding, ipady=5)


    
    # result1= LabelFrame(resultframe1, bg='blue')
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)
    # result1= LabelFrame(resultframe1)
    # result1.pack(**padding, ipadx=100, side=LEFT, fill=Y)

search_btn.config(command=show_results)

root.mainloop()