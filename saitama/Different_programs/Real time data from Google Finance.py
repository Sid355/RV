#url=https://www.google.com/finance/quote/MCX:NSE?hl=en


import requests
from bs4 import BeautifulSoup
import time

ticker = 'MCX'
url=f'https://www.google.com/finance/quote/{ticker}:NSE?hl=en'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
