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
# stock_info = ts.get_stock_basics()
stock_info = get_index_stocks('000300.XSHG')

def find_largest_corr(research_sid,end_date,scan_first_end_date,scan_last_end_date,interval):
    # 获取research历史数据
    target_info = get_security_info(research_sid)
    
    print("研究目标：" + target_info.display_name + " 开始日期：" + str(end_date - datetime.timedelta(days=interval)) + " 结束时间：" + str(end_date))
    df_research = get_bars(research_sid, interval, unit='1d',fields=['date','open','high','low','close'],include_now=False,end_dt=end_date)
    # research股票每日涨跌幅
    df_research['Daily_Return'] = df_research['close'].pct_change()
    df_research['Daily_Return'].index = [i for i in range(df_research['Daily_Return'].shape[0])]
    print(df_research['Daily_Return'])
    print("回测扫描开始日期：" + str(scan_first_end_date - datetime.timedelta(days=interval)) + " 结束时间：" + str(scan_last_end_date))
    delta = datetime.timedelta(days=1)
    weekend = set([5, 6])
    max_corr = 0
    max_corr_sid = ""
    max_corr_start = ""
    max_corr_end = ""
    # 创建一个空的Dataframe
    result = pd.DataFrame(columns=('sid', 'name', 'start', 'end', 'corr'))
    for i in stock_info.code[0:1]:
        each_corr = 0
        each_start = ""
        each_end = ""
        b_start_date = bm_start_date
        if i == research_sid:
            continue
        while b_start_date < bm_last_start_date:
            #跳过周末
            if b_start_date.weekday() in weekend:
                b_start_date += delta
                continue
            b_start = str(b_start_date)[0:10]
            b_end_date = b_start_date + dt.timedelta(days=interval)
            b_end = str(b_end_date)[0:10]
            # 获取benchmark历史数据
            df_benchmark = ts.get_hist_data(i, start=b_start, end=b_end)
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
                each_start = b_start
                each_end = b_end
            if  corr.iloc[1][0] > max_corr:
                max_corr = corr.iloc[1][0]
                max_corr_start = b_start
                max_corr_end = b_end
                max_corr_sid = i
            # list_date.append(b_start)
            # list_corr.append(abs(corr.iloc[1][0]))
            b_start_date += delta
        # datas = pd.DataFrame({'日期': list_date, '相关系数': list_corr})
        # sns.lineplot(x='日期', y='相关系数', ci=None, data=datas)
        name = basic_data.loc[i]['name']
        print(str(i) + "-" + name + ":" + str(each_corr))
        result = result.append(pd.DataFrame({'sid': [i], 'name': [name], 'start': [each_start], 'end': [each_end], 'corr':[each_corr]}),ignore_index=True)

    print("max correlation exists with : " + max_corr_sid + "-" + basic_data.loc[max_corr_sid]['name'] + " : " + str(max_corr) + "(" + max_corr_start +"至" + max_corr_end + ")")
    result = result.sort_values(by=['corr'],ascending=False)
    print(result)
    # CandlestickPlot.plot_candlestick(max_corr_sid, max_corr_start, max_corr_end)
    CandlestickPlot.plot_candlestick_compare(research_sid, start, end,max_corr_sid, max_corr_start, max_corr_end)

