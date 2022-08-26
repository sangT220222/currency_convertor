from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from forex_python.converter import CurrencyRates

#root master 
root = Tk()

# Framework
## create tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=5)

currency_frame = Frame(my_notebook, width = 480, height = 480)
conversion_frame = Frame(my_notebook, width = 480, height = 480)


def set_gui_title():
    root.title('Currency Converter')
    
def set_gui_window_size():
    root.geometry('500x500')


currency_frame.pack(fill='both', expand=1)

conversion_frame.pack(fill='both', expand=1)

def add_tabs_to_gui():
    my_notebook.add(currency_frame, text='Currencies')
    my_notebook.add(conversion_frame, text='Convert')

# Currency tab
home_currency_text = LabelFrame(currency_frame, text = "Your home currency")
home_currency_text.pack(pady = 20)

conversion_text = LabelFrame(currency_frame, text='Conversion Currency')
conversion_text.pack(pady = 20)

button_frame = Frame(currency_frame)
button_frame.pack(pady=20)

home_entry_box = Entry(home_currency_text, font=('Helvetica', 24))
home_entry_box.pack(padx = 10, pady = 10)

conversion_label = Label(conversion_text, text = 'Currency to convert to')
conversion_label.pack(pady=10)

conversion_entry = Entry(conversion_text , font= ('Helvetica', 24))
conversion_entry.pack(pady=10, padx=10)

 
rate_label = Label(conversion_text, text = 'Currency conversion rate')
rate_label.pack(pady=20)

rate_entry = Entry(conversion_text , font= ('Helvetica', 24), bd=0, bg='systembuttonface')
rate_entry.pack(pady=10, padx=10)

def disabling_conversion_tab():
    my_notebook.tab(1, state = 'disabled')

def lock():
    if not home_entry_box.get() or not conversion_entry.get():
        messagebox.showwarning('Warning', 'You need to fill out all the fields before locking')
    elif check_for_home_currency_input() == 1:
        messagebox.showwarning('Warning', 'Home currency isn\'t valid')
    elif check_for_currency_to_convert_to_input() == 1:
        messagebox.showwarning('Warning', 'Currency to convert to isn\'t valid')
    else:
        #Disable entry boxes
        home_entry_box.config(state = 'disabled')
        conversion_entry.config(state = 'disabled')
        #display conversion rate    
        insert_conversion_rate()
        rate_entry.config(state = 'disabled')
        #Enable tab
        my_notebook.tab(1, state = 'normal') #1 represents our 2nd tab which is "Convert"
        amount_label_frame.config(text=f'Amount of {get_home_currency_input()} to convert to {get_currency_to_convert_to()}')
        converted_label_frame.config(text=f'Equales this many {get_currency_to_convert_to()}')
        convert_button.config(text=f'Convert from {get_home_currency_input()}')

def unlock():
        # Enable entry boxes
        home_entry_box.config(state = 'normal')
        conversion_entry.config(state = 'normal')
        rate_entry.config(state = 'normal')
        #Disable tab
        my_notebook.tab(1, state = 'disabled')

def add_lock_button(): 
    lock_button = Button(button_frame, text = 'Lock', command = lock)
    lock_button.grid(row=0, column = 0 , padx =10)

def add_unlock_button(): #
    unlock_button = Button(button_frame, text = 'Unlock', command = unlock)
    unlock_button.grid(row=0, column = 1 , padx =10)

#Conversion tab      
def convert():
    converted_entry.delete(0,END)
    converted_entry.insert(0, formated_conversion_final())

amount_label_frame = LabelFrame(conversion_frame, text = 'Amount to convert')
amount_label_frame.pack(pady=20)

converted_label_frame = LabelFrame(conversion_frame, text='Converted Currency')
converted_label_frame.pack(pady=20)

amount_entry_box = Entry(amount_label_frame, font=('Helvetica', 24))
amount_entry_box.pack(pady=10, padx=10)

converted_entry = Entry(converted_label_frame, font=('Helvetica', 24), bd=0, bg='systembuttonface')
converted_entry.pack(pady=10,padx=10)

convert_button = Button(amount_label_frame, text='Convert', command = convert)
convert_button.pack(pady=20)

def clear():
    amount_entry_box.delete(0, END)
    converted_entry.delete(0, END)

def add_clear_button():
    clear_button = Button(conversion_frame, text='Clear', command = clear)
    clear_button.pack(pady=20)

def add_spacing():
    spacer = Label(conversion_frame, text='', width=69)
    spacer.pack()

# Using Forex python library
currency = CurrencyRates()
currencies_list = [c for c in currency.get_rates('USD')]
currencies_list += ['USD']

def get_home_currency_input():
    home_currency_input = home_entry_box.get().upper()
    return home_currency_input
    
def get_currency_to_convert_to():
    currency_to_convert_to = conversion_entry.get().upper()
    return currency_to_convert_to

def get_amount_for_conversion():
    amount_for_conversion = int(amount_entry_box.get())
    return amount_for_conversion

def conversion():
    final_result = float(currency.convert(get_home_currency_input(), get_currency_to_convert_to(), get_amount_for_conversion()))
    return final_result

def rounding_conversion_to_2_dp():
    rounded_result = round(conversion() , 2)
    return rounded_result

def formated_conversion_final():
    final_conversion = '{:,}'.format(rounding_conversion_to_2_dp())
    return final_conversion

def get_rate():
    rate_of_currency_input = round(currency.get_rate(get_home_currency_input(),get_currency_to_convert_to()),5)
    return rate_of_currency_input

def insert_conversion_rate():
    rate_entry.delete(0,END)
    rate_entry.insert(0 , get_rate())

def check_for_home_currency_input():
    for c in currencies_list:
        if get_home_currency_input() == c:
            return 0
    return 1

def check_for_currency_to_convert_to_input():
    for c in currencies_list:
        if get_currency_to_convert_to() == c:
            return 0
    return 1

if __name__ == '__main__':
    set_gui_title()
    set_gui_window_size()
    add_tabs_to_gui()
    add_lock_button() 
    add_unlock_button()
    add_clear_button()
    add_spacing()
    disabling_conversion_tab()
    root.mainloop()
