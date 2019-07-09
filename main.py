import plotKline
import datetime

stock_id = '600519.XSHG'
end_date = datetime.date.today()
interval = 30
interval_day = datetime.timedelta(days=interval)
start_date = end_date - interval_day
plotKline.plotCandlesticks(stock_id,start_date,end_date,stock_id,start_date,end_date,interval)
