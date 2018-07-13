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
    pandas.set_option('display.max_rows',None)
    pandas.set_option('display.max_column', None)
    pandas.set_option('display.width', 2000)

    for year in range(2013,2019,1):
        for quarter in range(1,5,1):
            print(str(year) + "-" + str(quarter) + ":")
            df_report = ts.get_report_data(year,quarter)
            df_profit = ts.get_profit_data(year,quarter)
            df_operation = ts.get_operation_data(year,quarter)
            print(df_report.shape)
            print(df_profit.shape)
            print(df_operation.shape)
            df_growth = ts.get_growth_data(year, quarter)
            df_debtpay = ts.get_debtpaying_data(year, quarter)
            df_cashflow = ts.get_cashflow_data(year, quarter)
            # df_report = df_report[df_report['code']=='603609']
            # df_profit = df_profit[df_profit['code']=='603609']
            # df_operation = df_operation[df_operation['code']=='603609']
            tempdf = pandas.merge(df_report, df_profit, how='outer', on=['code', 'name'])
            tempdf = pandas.merge(tempdf, df_operation, how='outer', on=['code', 'name'])
            tempdf = pandas.merge(tempdf, df_growth, how='outer', on=['code', 'name'])
            tempdf = pandas.merge(tempdf, df_debtpay, how='outer', on=['code', 'name'])
            result_df = pandas.merge(tempdf, df_cashflow, how='outer', on=['code', 'name'])
            result_df = result_df.drop_duplicates(subset=['code'], keep='first')
            result_df['year'] = year
            result_df['quarter'] = quarter
            cols = list(result_df)
            cols.insert(0,cols.pop(cols.index('year')))
            cols.insert(1,cols.pop(cols.index('quarter')))
            result_df = result_df.ix[:,cols]
            #print(df)
            engine = create_engine('mysql+pymysql://root:@localhost:3306/test?charset=utf8')
            result_df.to_sql('hist_basic',engine,if_exists='append',dtype={'code':VARCHAR(6),'name':VARCHAR(20)})
            if  year == 2013 and quarter == 1:
                with engine.connect() as con:
                    con.execute("ALTER TABLE `hist_basic` ADD PRIMARY KEY(`year`,`quarter`,`code`);")

main()