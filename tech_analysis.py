#coding:utf-8
"""
 技术分析

by 葛毅杰 - 2018-07-13
"""
import datetime

import numpy
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.linearmodels as snsl

class tech_analysis:
    # 计算股价相关性
    def tech_correlation(self,stock_list,start,end):
        stock_df = pd.DataFrame()
        for stock in stock_list:
            closing_df = ts.get_hist_data(stock, start, end)['close']
            stock_df = stock_df.join(pd.DataFrame({stock: closing_df}), how='outer')
        result_df = stock_df.pct_change()
        snsl.corrplot(result_df.dropna())

    # 得到金叉股票列表
    def tech_jincha(self):
        # 站上5日线
        def zs5(his):
            ma_n = pd.rolling_mean(his, 5)
            temp = his - ma_n
            # temp_s包含了前一天站上五日线的股票代码
            temp_s = list(temp[temp > 0].iloc[-1, :].dropna().index)
            return temp_s
        # 站上10日线
        def zs10(his):
            ma_n = pd.rolling_mean(his, 10)
            temp = his - ma_n
            temp_s = list(temp[temp > 0].iloc[-1, :].dropna().index)
            return temp_s
        # 金叉突破
        def jc(his):
            mas = pd.rolling_mean(his, 5)
            mal = pd.rolling_mean(his, 10)
            temp = mas - mal
            # temp_jc昨天大于0股票代码
            # temp_r前天大于0股票代码​
            temp_jc = list(temp[temp > 0].iloc[-1, :].dropna().index)
            temp_r = list(temp[temp > 0].iloc[-2, :].dropna().index)
            temp = []
            for stock in temp_jc:
                if stock not in temp_r:
                    temp.append(stock)
            return temp

        # 确定时间范围
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        start_date = datetime.datetime.now() - datetime.timedelta(days=5)
        start_date = start_date.strftime('%Y-%m-%d')
        # 得到需要遍历的股票列表
        #base_df = ts.get_concept_classified()
        base_df = ts.get_sz50s()
        stock_list = numpy.array(base_df['code'])
        his = pd.DataFrame()
        for stock in stock_list:
            each_his = ts.get_hist_data(stock, start=start_date, end=end_date)
            his.append(each_his)
        # 求三种条件下的股票代码交集
        con1 = zs5(his)
        con2 = zs10(his)
        con3 = jc(his)
        result_stock_list = list(set(con1).intersection(set(con2)).intersection(set(con3)))

        return result_stock_list



if __name__ == "__main__":
    ta = tech_analysis()
    # 相关系数
    # ta.tech_correlation(['601330','603348'],'2018-06-15','2018-07-12')
    # plt.show()
    # 金叉列表
    print(ta.tech_jincha())