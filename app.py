from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'card-block'})

row = table.find_all('tr')

row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    
    row = table.find_all('tr')[i]
    period = row.find('th').text
    x = row.find_all('td')
    market_cap = x[0].text.strip()
    volume = x[1].text.strip()
    open_value = x[2].text.strip()
    close = x[3].text.strip()
    temp.append((period, market_cap, volume, open_value, close)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date','Market Cap','Volume','Open','Close' ))

#insert data wrangling here
df_ready = df[['Date','Volume']]
df_ready['Date'] = df_ready['Date'].astype('datetime64')
df_ready['Volume'] = df_ready['Volume'].str.replace('$','').str.replace(',','')
df_ready['Volume'] = df_ready['Volume'].astype('float64')
df_ready = df_ready.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df_ready["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df_ready.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)