
# coding: utf-8
import pandas as pd
import json
import requests
import streamlit as st
import time
import akshare as ak
from apscheduler.schedulers.blocking import BlockingScheduler

#大盘最新价格
df_cy = pd.DataFrame()
df_cy = ak.stock_zh_a_spot_em()
#先获取当前日期，格式8-29：周一
xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
riqi = time.strftime("%m-%d-%H-%M", time.localtime())
xingqi = time.strftime("%w", time.localtime())
riqi = riqi + ":" + xq_list[int(xingqi)]

gpgz_file = "./data/gpgz.json"#连接JSON数据库文件：股票跟踪
with open(gpgz_file) as f:
	gpgz = json.load(f)#读取JSON文件的信息，转化为字典

gpxx_cy = {} #创建所有股票的汇总数据字典,持有股票信息
for cygpdm in gpgz:
	cygg = df_cy[cygpdm]
	xulie = (1,2,3,8,11,16)#需要获取req_list中的元组中6个位置的数据：股票名称、当前价、当日涨幅、换手率、最低价、流通股市值
	cy_gpxx = []  # 创建股票信息列表，存储单个股票以上6个需要数据
	for i in xulie:
		cy_gpxx.append(cygg[i])
print(cy_gpxx)





		#以下代码判断股票缺口是否已经消失和计算缺口距离-----------------------------------------------
		#dqjg = float(gpxx[1]) #当前价格变量--------将字符串转化为浮点数
		#zdjg = float(gpxx[4]) #当日最低价格
		#qkxd = float(js_gp[gpdm][0]) #缺口下端价格
		#qksd = float(js_gp[gpdm][1]) #缺口上端价格
'''
		if zdjg < qkxd:
			wqxs = '√'#变量wqxs的意思是：完全消失
		else:
			wqxs = '×'

		if zdjg  < qksd:
			bfxs = '√'#变量bfxs的意思是：部分消失
		else:
			bfxs = '×'
		gpxx.append(bfxs)
		gpxx.append(wqxs)
		#以下代码添加当前股价与缺口上端的距离百分比
		qkjl = (dqjg-qksd)/dqjg*100
		gpxx.append(str("%.1f" % qkjl)+'%')
		gpxx.append(hy_js[gpdm])
		gpxx_hz[gpdm] = gpxx
	gpxx_df = pd.DataFrame(gpxx_hz) #建立整个股票信息的DataFrame
	gpxx_df.index = ['名称', '当前价格', '当前涨幅', '换手率', '当日最低', '流通市值', '部分消失', '完全消失',
					 '缺口距离','行业']
	ww = gpxx_df.T

	st.dataframe(ww.iloc[::-1]) #  .T  将dataframe的行和列进行了互换

	st.markdown("---")#画一条水平线
	st.write("1→2→3→5→8→13→21→34→55→89→144→233")#画一条水平线
'''
time_printer()

