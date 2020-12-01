from datetime import datetime
import requests

purchase_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # format: '11/26/2020, 19:08:35'
twelvedata_key = '385f19abc1974040a8f0ea2b58371506'

price_url = "https://api.twelvedata.com/price?symbol={0}&apikey={1}".format('AAPL', twelvedata_key)
real_time_price = requests.get(price_url)
real_time_price.json()['price']
