import requests
from tkinter import *

# Global parameters
invest_result = 0
total_cost  = 0
total_value = 0

twelvedata_key = 'API KEY'

# Get my purchase records
record_url = "MY API URL"
record_response = requests.get(record_url)
my_all_stock = record_response.json()

for i in my_all_stock['Shares']:
    # Purchase info
    p_symbol  = i['Transactioin Symbol']
    p_units   = i['Transactioin Volumns']
    p_price   = i['Transactioin Price']

    # Get the real-time price
    price_url = "https://api.twelvedata.com/price?symbol={0}&apikey={1}".format(p_symbol, twelvedata_key)
    real_time_price = requests.get(price_url)
    r_price = float(real_time_price.json()['price'])

    # Calculate real-time profit or loss
    # print(p_price, p_units, type(p_price), type(p_units))
    total_cost  += (p_price * p_units)

    #print(r_price, p_units, type(r_price), type(p_units))
    total_value += (r_price * p_units)

invest_result = (total_value - total_cost)
# print("Total invest: {0}, Current Market Values: {1}, Evaluate Current Investment: {2}".format(total_cost, total_value, invest_result))


# Generate GUI Dash
root=Tk()

root.title("My Stocks Tracker")

# Total Invest
label_invest = Label(root, text="Total Invest", relief=RAISED, bg='brown')

invest_num = total_cost
label_invest_num = Label(root, text=invest_num, relief=FLAT, bg='white')

label_invest.grid(row = 0, column = 0, sticky = W, pady = 2)
label_invest_num.grid(row = 1, column = 0, sticky = W, pady = 2)

# Current Market Values
label_marketValues = Label(root, text="Current Market Values", relief=RAISED, bg='green')

current_num = total_value
label_marketValues_num = Label(root, text=current_num, relief=FLAT, bg='white')

label_marketValues.grid(row = 2, column = 0, sticky = W, pady = 2)
label_marketValues_num.grid(row = 3, column = 0, sticky = W, pady = 2)

# Result
label_overview = Label(root, text="Investment Result", relief=RAISED, bg='black', fg='white')

result_num = invest_result
label_overview_num = Label(root, text=result_num, relief=FLAT, bg='white')

label_overview.grid(row = 4, column = 0, sticky = W, pady = 2)
label_overview_num.grid(row = 5, column = 0, sticky = W, pady = 2)

# set an infinite loop so window stays in view
root.mainloop()
