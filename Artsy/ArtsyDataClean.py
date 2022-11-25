import pandas as pd
import numpy as np
import os
import re

usd, pound, eur = "$", "£", "€"
# To change work_year to numeric
def work_year(df):
    for i in range(len(df['work_year'])):
        if not df['work_year'][i].isnumeric():
            df['work_year'][i] = df['work_year'][i][-4:]
    df['work_year'] = df['work_year'].astype(int)
    return df
#helper
def toUsd(currency, amount):
    if currency == "pound":
        return amount*1.21
    if currency == "eur":
        return amount*1.04
    else:
        return amount
#helper
def getPrice (price):
    if not isinstance(price, str):
        return price
    if '.' in price:
        print("error:", price)
    if pound in price:
        currency = "pound"
    if eur in price:
        currency = "eur"
    else:
        currency = "usd"
    price_list = price.split("–")
    if len(price_list) > 2:
        print("error: ",price_list)
        return
    if len(price_list) == 1:
        amount =  ''.join(c for c in price if c.isdigit())
        return toUsd(currency,int(amount))
    else:
        amount1 =  ''.join(c for c in price_list[0] if c.isdigit())
        amount2 =  ''.join(c for c in price_list[1] if c.isdigit())
        amount = (int(amount1)+ int(amount2))//2
        return toUsd(currency,amount)
    


def main():
    cur_path = os.getcwd()
    result_path = 'ArtsyResult'
    file_name = 'ArtsyData.csv'
    clean_file_name = 'CleanedArtsyData.csv'
    path = os.path.join(cur_path,result_path,file_name)
    df = pd.read_csv(path)
    # drop all incomplete 
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)
    # change work_year to numeric
    df = work_year(df)
    # observation: all prices are in unit usd, gbp or eur
    # To change price to number; estimated price to an actual number
    for i in range(len(df['price'])):
        df['price'][i] = getPrice(df['price'][i])
    filepath = path = os.path.join(cur_path,result_path,clean_file_name)
    df.to_csv(filepath, index=False)

if __name__ == '__main__':
    main()