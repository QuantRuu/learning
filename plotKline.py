from jqdatasdk import *
import pyecharts.options as opts
from pyecharts.charts import Kline,Page,Line

auth('13917211596','910722mu')
page = Page()

# 定义k线图的提示框的显示函数
def show_kline_data(params):
  param = params[0]
  if param.data[4]:
    return "date = " + param.name + "<br/>" + "open = " + param.data[1] + "<br/>" + "close = " + param.data[
  2] + "<br/>" + "high = " + param.data[3] + "<br/>" + "low = " + param.data[
    4] + "<br/> "
  else:
    return "date = " + param.name + "<br/>" + "cci = " + param.value + "<br/>"


def getSingleCandlestick(stock_id, end_date, interval):
  # get stock trade info from jqdata
  stock_info = get_security_info(stock_id)
  data = get_bars(stock_id, interval, unit='1d',fields=['date','open','high','low','close'],include_now=False,end_dt=end_date)
  # print(data)
  # 画出K线图
  price = [[open, close, lowest, highest] for open, close, lowest, highest in
  zip(data['open'], data['close'], data['low'], data['high'])]
  kline = Kline()
  kline.add_xaxis(list(data['date']))
  kline.add_yaxis(
    '日线',
    price,
    itemstyle_opts=opts.ItemStyleOpts(
      color="#FF6347",
      color0="#BCEE68",
      border_color="#8A0000",
      border_color0="#008F28",
    )
  )
  kline.set_global_opts(
      xaxis_opts=opts.AxisOpts(is_scale=True),
      yaxis_opts=opts.AxisOpts(
          is_scale=True,
          splitarea_opts=opts.SplitAreaOpts(
              is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
          ),
      ),
      datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
      title_opts=opts.TitleOpts(title=stock_id + "-" + stock_info.display_name),
  )

  page.add(kline)


def plotCandlesticks(research_id, start_date, end_date, benchmark_id, b_start_date, b_end_date, interval):
  getSingleCandlestick(research_id,end_date, interval)
  getSingleCandlestick(benchmark_id,b_end_date, interval)
  page.render()

