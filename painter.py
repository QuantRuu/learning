#coding:utf-8
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.linearmodels as snsl
from datetime import datetime
import numpy

def get_price_data(code):
    end = datetime.today()
    start = datetime(end.year-5,end.month,end.day)
    str_end = str(end)[0:10]
    str_start = str(start)[0:10]
    stock_df = ts.get_hist_data(code,str_start,str_end)
    if stock_df is None:
        stock_df['daily_return'] = ''
    else:
        stock_df['daily_return'] = stock_df['close'].pct_change()
    #stock_df['daily_return'].plot(legend=True, figsize=(8,5))
    #sns.distplot(stock_df['daily_return'].dropna(),bins=100)
    return stock_df

def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_column', None)
    pd.set_option('display.width', 2000)
    sns.set_style('darkgrid')
    stock_df = ts.get_industry_classified()
    stock_list = stock_df[stock_df['c_name']=='金融行业']['code']
    stock_arr = numpy.array(stock_list)
    result_df = pd.DataFrame()
    for stock in stock_arr:
        closing_df = get_price_data(stock)['close']
        result_df = result_df.join(pd.DataFrame({stock:closing_df}),how='outer')
    tech_rets = result_df.pct_change()
    rets = tech_rets.dropna()
    plt.scatter(rets.std(),rets.mean())
    plt.ylabel('Excepted Return')
    plt.xlabel('Risk')
    for label, x, y in zip(rets.columns,rets.std(),rets.mean()):
        # 添加标注
        plt.annotate( label, xy =(x,y),xytext=(15,15), textcoords = 'offset points', arrowprops = dict(arrowstyle = '-',connectionstyle = 'arc3,rad=-0.3'))
    plt.show()

main()


