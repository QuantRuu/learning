#coding:utf-8
import os
import re

import pandas
from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
import tushare as ts
from sqlalchemy import create_engine, VARCHAR
import pymysql

def main():
    #df = ts.realtime_boxoffice()
    #df = ts.day_boxoffice()
    pandas.set_option('display.max_rows',None)
    pandas.set_option('display.max_column', None)
    pandas.set_option('display.width', 2000)
    #pandas.set_option('display.max_column', None)

    stock_list = ts.get_sz50s()
    print(stock_list)
    for row_index in stock_list.index:
        print('row_index:' + str(row_index))
        stock_code = stock_list.loc[row_index].values[1] + ''
        stock_name = stock_list.loc[row_index].values[2] + ''
        print(stock_code + " : " + stock_name)
        df = ts.get_hist_data(stock_code,'2013-07-01')
        if df.empty:
            continue
        df['stock_code'] = stock_code
        df['stock_name'] = stock_name
        cols = list(df)
        cols.insert(0,cols.pop(cols.index('stock_code')))
        cols.insert(1,cols.pop(cols.index('stock_name')))
        df = df.ix[:,cols]
        #print(df)
        engine = create_engine('mysql+pymysql://root:@localhost:3306/test?charset=utf8')
        df.to_sql('hist_price',engine,if_exists='append',dtype={'date':VARCHAR(df.index.get_level_values('date').str.len().max()),'stock_code':VARCHAR(6),'stock_name':VARCHAR(20)})
        if  row_index == 1:
            with engine.connect() as con:
                con.execute("ALTER TABLE `hist_price` ADD PRIMARY KEY(`date`,`stock_code`);")

main()