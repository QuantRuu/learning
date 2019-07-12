from jqdatasdk import *
import pyecharts.options as opts
import datetime
from pyecharts.charts import Kline,Page,Line,Bar,Grid
from pyecharts.globals import ThemeType

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
  data = get_price(stock_id, count=interval, end_date=end_date, frequency='1d', fields=['open','high','low','close','volume'])
  # print(data)
  # 画出K线图
  price = [[open, close, lowest, highest] for open, close, lowest, highest in
  zip(data['open'], data['close'], data['low'], data['high'])]
  x_list = []
  for i in data.index:
    x_list.append(str(i)[0:10])
  kline = Kline()
  kline.add_xaxis(x_list)
  kline.add_yaxis(
    '日线',
    price,
    markpoint_opts=opts.MarkPointOpts(
      data=[opts.MarkPointItem(name="endpoint",coord=[x_list[len(x_list)-interval-1],price[len(x_list)-interval-1]],value=price[len(x_list)-interval-1])]
    ),
    markline_opts=opts.MarkLineOpts(
      data=[opts.MarkLineItem(type_="max", value_dim="close")]
    ),
    # itemstyle_opts=opts.ItemStyleOpts(
    #   color="#FF6347",
    #   color0="#BCEE68",
    #   border_color="#8A0000",
    #   border_color0="#008F28",
    # )
  )
  kline.set_global_opts(
      xaxis_opts=opts.AxisOpts(is_scale=True, is_show=False),
      yaxis_opts=opts.AxisOpts(
          is_scale=True,
          splitarea_opts=opts.SplitAreaOpts(
              is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
          ),
      ),
      datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%"),opts.DataZoomOpts(xaxis_index=[0,1],type_="inside")],
      title_opts=opts.TitleOpts(title=stock_id + "-" + stock_info.display_name),
      legend_opts=opts.LegendOpts(is_show=False),
  )
  

  volume = list(data['volume'])
  bar = Bar()
  bar.add_xaxis(x_list)
  bar.add_yaxis("成交量",volume,color=["#BCEE68"])
  bar.set_global_opts(
    yaxis_opts=opts.AxisOpts(split_number=3),
    legend_opts=opts.LegendOpts(is_show=False),
  ).set_series_opts(
    label_opts=opts.LabelOpts(is_show=False),
  )

  grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
  grid.add(kline,grid_opts=opts.GridOpts(pos_bottom="28%"))
  grid.add(bar,grid_opts=opts.GridOpts(pos_top="74%"))
  page.add(grid)


def plotCandlesticks(research_id, end_date, benchmark_id, b_end_date, interval):
  getSingleCandlestick(research_id,end_date, interval)
  b_end = b_end_date + datetime.timedelta(days=interval)
  getSingleCandlestick(benchmark_id,b_end, interval*2)
  page.render()

