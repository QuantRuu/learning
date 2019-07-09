from jqdatasdk import *
import pyecharts.options as opts
from pyecharts.charts import Kline

auth('13917211596','910722mu')
# get stock trade info from jqdata
data = get_bars('600519.XSHG', 100, unit='1d',fields=['date','open','high','low','close'],include_now=False,end_dt='2019-07-07')
print(data)

# 定义k线图的提示框的显示函数
def show_kline_data(params):
  param = params[0]
  if param.data[4]:
    return "date = " + param.name + "<br/>" + "open = " + param.data[1] + "<br/>" + "close = " + param.data[
  2] + "<br/>" + "high = " + param.data[3] + "<br/>" + "low = " + param.data[
    4] + "<br/> "
  else:
    return "date = " + param.name + "<br/>" + "cci = " + param.value + "<br/>"


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
    title_opts=opts.TitleOpts(title="Kline"),
)

kline.render()



