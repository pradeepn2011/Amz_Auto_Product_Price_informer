import requests  
from bs4 import BeautifulSoup 
import smtplib
import csv
from datetime import datetime
from dateutil.tz import gettz
import pytz
import os
import time

url = 'https://www.amazon.in/HP-Processor-Windows-Natural-14s-dq2535TU/dp/B0928NL6F3/ref=sr_1_3?crid=TDQZ7CVY7YP0&dchild=1&keywords=hp+14+2021+11th+gen+intel+core+i5+laptop&qid=1635607127&sprefix=hp+14+2021+11th+gen+intel+core+i5+laptop%2Caps%2C273&sr=8-3'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

def check_lappy_price():

    page = requests.get(url, headers=headers)

    bs = BeautifulSoup(page.content, 'html.parser') #lxml
    
    product_title = bs.find(id = "productTitle")
    if product_title:
        product_title = product_title.get_text()
        print("product_title found: ", product_title)
    else:
        print("product_title was not found in page.content")
    
    
    price = bs.find(id = "priceblock_dealprice").get_text()
    if price:
        price = price.get_text()
    #id=priceblock_ourprice or id=priceblock_dealprice, 
    #note: id keeps changing based on offer
    #price = bs.find(id = "priceblock_dealprice").get_text() #priceblock_dealprice, priceblock_ourprice
    
    price = price[1:7]
    price_float =  float(price.replace(",",""))
    print("price now is : ", price_float)
    
    file_exist = True

    if not os.path.exists('./data/lappy_price.csv'):
        file_exist = False
        
    with open("./data/lappy_price.csv","a") as file:
            writer = csv.writer(file, lineterminator='\n')
            fields = ["Timestamp","price"]
            
            if not file_exist:
                writer.writerow(fields)
                       
            #UTC = pytz.utc
            #IST = pytz.timezone('Asia/Kolkata')
            #datetime_ist = datetime.now(IST)
            #timestamp = datetime_ist.strftime('%d:%m:%Y %H:%M:%S %Z %z')
            
            timestamp =datetime.now(tz=gettz('Asia/Kolkata'))
            writer.writerow([timestamp, price_float])
            
            print("***** Wrote data in to file @ *****", timestamp)
    
    return price_float

while True:
    
    price = check_lappy_price()
    if(price < 50000):
        print("Laptop now is under my 50k budget \n")
        break
    else:
        print("***** I need to wait for few more days ***** \n")
        break
    #time.sleep(10)
