from jqdatasdk import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotKline
sns.set_style('whitegrid',{'font.sans-serif':['simhei','Arial']})

sid_gzmt = '600519' #贵州茅台
sid_wly = '000858' #五粮液
sid_gldq = '000651' #格力电器
stock_info = get_index_stocks('000300.XSHG')

def find_largest_corr(research_sid,end_date,scan_first_end_date,scan_last_end_date,interval):
    # 获取research历史数据
    target_info = get_security_info(research_sid)
    
    print("研究目标：" + target_info.display_name + " 开始日期：" + str(end_date - datetime.timedelta(days=interval)) + " 结束时间：" + str(end_date))
    df_research = get_bars(research_sid, interval, unit='1d',fields=['date','open','high','low','close'],include_now=False,end_dt=end_date)
    # research股票每日涨跌幅
    df_research['Daily_Return'] = df_research['close'].pct_change()
    df_research['Daily_Return'].index = [i for i in range(df_research['Daily_Return'].shape[0])]
    # print(df_research['Daily_Return'])
    print("回测扫描开始日期：" + str(scan_first_end_date - datetime.timedelta(days=interval)) + " 结束时间：" + str(scan_last_end_date))
    delta = datetime.timedelta(days=1)
    weekend = set([5, 6])
    max_corr = 0
    max_corr_sid = ""
    max_corr_start = ""
    max_corr_end = ""
    # 创建一个空的Dataframe
    result = pd.DataFrame(columns=('sid', 'name', 'start', 'end', 'corr'))
    # for i in stock_info:
    for i in ["000656.XSHE"]:
        each_corr = 0
        each_start = ""
        each_end = ""
        test_end_date = scan_first_end_date
        if i == research_sid:
            continue
        while test_end_date < scan_last_end_date:
            #跳过周末
            if test_end_date.weekday() in weekend:
                test_end_date += delta
                continue
            # 获取benchmark历史数据
            df_benchmark = get_bars(i, interval, unit='1d',fields=['date','open','high','low','close'],include_now=False,end_dt=test_end_date)
            # benchmark股票每日涨跌幅
            df_benchmark['Daily_Return'] = df_benchmark['close'].pct_change()
            df_benchmark['Daily_Return'].index = [i for i in range(df_benchmark['Daily_Return'].shape[0])]
            # 合并
            df = pd.concat([df_research['Daily_Return'], df_benchmark['Daily_Return']], axis=1,
                           keys=['research_return', 'benchmark_return'], sort=False)
            # 填充缺失数据
            df.ffill(axis=0, inplace=True)
            corr = df.corr(method='pearson', min_periods=1)
            if  corr.iloc[1][0] > each_corr:
                each_corr = corr.iloc[1][0]
                each_end = test_end_date
            if  corr.iloc[1][0] > max_corr:
                max_corr = corr.iloc[1][0]
                max_corr_end = test_end_date
                max_corr_sid = i
            test_end_date += delta
        # datas = pd.DataFrame({'日期': list_date, '相关系数': list_corr})
        # sns.lineplot(x='日期', y='相关系数', ci=None, data=datas)
        target_info = get_security_info(i)
        name = target_info.display_name
        print(str(i) + "-" + name + ":" + str(each_corr))
        result = result.append(pd.DataFrame({'sid': [i], 'name': [name], 'start': [each_start], 'end': [each_end], 'corr':[each_corr]}),ignore_index=True)

    max_security_info = get_security_info(max_corr_sid)
    print("max correlation exists with : " + max_corr_sid + "-" + max_security_info.display_name + " : " + str(max_corr) + "(" + str(max_corr_end) + "往前"+str(interval)+"个交易日)")
    result = result.sort_values(by=['corr'],ascending=False)
    print(result)
    plotKline.plotCandlesticks(research_sid,end_date,max_corr_sid, max_corr_end, interval)

