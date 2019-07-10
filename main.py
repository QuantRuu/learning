import plotKline
import datetime
import correlation

stock_id = '600519.XSHG'
end_date = datetime.date.today()
interval = 30
interval_day = datetime.timedelta(days=interval)
start_date = end_date - interval_day
# plotKline.plotCandlesticks(stock_id,start_date,end_date,stock_id,start_date,end_date,interval)

scan_first_end_date = start_date - datetime.timedelta(days=interval * 2)
scan_last_end_date = start_date - datetime.timedelta(days=interval * 1)


correlation.find_largest_corr(stock_id, end_date, scan_first_end_date, scan_last_end_date, interval)
