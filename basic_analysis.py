#coding:utf-8
"""
 基本面分析

by 葛毅杰 - 2018-07-12
"""
import tushare as ts
import pandas as pd

class basic_analysis:
    # 预测高送转
    def basic_est_high_turn_to(self):
        basic = ts.get_stock_basics()
        hq = ts.get_today_all()
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_column', None)
        pd.set_option('display.width', 2000)
        # 当前股价,如果停牌则设置当前价格为上一个交易日股价
        hq['trade'] = hq.apply(lambda x: x.settlement if x.trade == 0 else x.trade, axis=1)
        # 分别选取流通股本,总股本,每股公积金,每股收益
        basedata = basic[['outstanding', 'totals', 'reservedPerShare', 'esp']]
        # 选取股票代码,名称,当前价格,总市值,流通市值
        hqdata = hq[['code', 'name', 'trade', 'mktcap', 'nmc']]
        # 设置行情数据code为index列
        hqdata = hqdata.set_index('code')
        # print('basedata:' + basedata.head(10))
        # print('hqdata:' + hqdata.head(10))
        # 合并两个数据表
        data = basedata.merge(hqdata, left_index=True, right_index=True)

        # 将总市值和流通市值换成亿元单位
        data['mktcap'] = data['mktcap'] / 10000
        data['nmc'] = data['nmc'] / 10000
        data.dropna()
        # 每股公积金>=5  and  流通股本<=3亿 and 每股收益>=5毛 and 总市值<100亿
        result = data[data['reservedPerShare']>=5]
        result = result[result['outstanding'] <= 3000]
        result = result[result['esp'] >= 0.5]
        result = result[result['mktcap'] <= 100]
        print('result:')
        print(result)


ba_obj = basic_analysis()
ba_obj.basic_est_high_turn_to()

