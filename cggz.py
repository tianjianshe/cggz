import pandas as pd
import streamlit as st
import json
import heapq
import time
import requests

#【持股跟踪】的信息列表
riqi = time.strftime("%m/%d", time.localtime())#获取当前日期
cggz_file = "./data/cggz.json"#连接JSON数据库文件：【持股跟踪】
with open(cggz_file) as f5:
	cggz_js = json.load(f5)#读取JSON文件的信息，转化为字典,获取【持股跟踪】写入的基本信息

hangye_file = "./data/hangye.json"#连接JSON数据库文件：个股行业查询
with open(hangye_file) as f5:
	hy_js = json.load(f5)#读取JSON文件的信息，转化为字典

st.sidebar.markdown("#### 功能栏")

with st.sidebar.expander("添加持有股票"):
	with st.form(key='my_form_cy'):
		gpdm_cy = st.text_input('持有股票代码')  #变量名的意思是：股票代码_持有
		gpsl_cy = st.text_input('股票数量')  #变量名的意思是：股票数量_持有
		gpcb_cy = st.text_input('股票成本')  #变量名的意思是：股票成本_持有
		submit_button = st.form_submit_button(label='提交')
		if gpdm_cy != "":
			with open(cggz_file, "w") as f:
				cggz_js[gpdm_cy] = [gpsl_cy,gpcb_cy,riqi,"-","-"]
				json.dump(cggz_js, f)

with st.sidebar.expander("修改成本价格"):
	with st.form(key='my_form_xg'):
		gpdm_xg = st.text_input('修改股票代码')  #变量名的意思是：股票代码_卖出
		cbjg_xg = st.text_input('修改成本价格')  #变量名的意思是：股票代码_卖出
		submit_button = st.form_submit_button(label='提交')
		if gpdm_xg != "":
			with open(cggz_file, "w") as f:
				cggz_js[gpdm_xg][1] = cbjg_xg
				json.dump(cggz_js, f)
with st.sidebar.expander("卖出持有股票"):
	with st.form(key='my_form_mc'):
		gpdm_mc = st.text_input('卖出股票代码')  #变量名的意思是：股票代码_卖出
		yked_mc = st.text_input('盈亏额度')  #变量名的意思是：股票代码_卖出
		submit_button = st.form_submit_button(label='提交')
		if gpdm_mc != "":
			with open(cggz_file, "w") as f:
				cggz_js[gpdm_mc][3] = riqi
				cggz_js[gpdm_mc][4] = yked_mc
				json.dump(cggz_js, f)

cggz_zb = {}#持股跟踪信息总表
for cs in cggz_js:
	url = 'https://hqm.stock.sohu.com/getqjson?code=cn_' + cs
	req = requests.get(url, timeout=30)  # 请求连接
	req = req.content  # 返回二进制数据
	req = req.decode('gb2312')  # 转换编码
	# 以下三行是获取字符串中的“[]”间的数据，其他数据不要
	nPos = req.index("[")
	nPos1 = req.index("]")
	req = req[nPos:nPos1 + 1]
	req_list = json.loads(req)  # 将字符串转化为json格式的数据
	xulie = (1, 2, 3, 4, 8, 9, 16)  # 需要获取req_list中的元组中6个位置的数据：股票名称、当前价、当日涨幅、今日涨额、换手率、量比、流通股市值
	cggz_gpxx = []  # 创建持股跟踪股票信息列表，存储单个股票以上7个需要数据
	for i in xulie:
		cggz_gpxx.append(req_list[i])
	ykfd = (float(cggz_gpxx[1])-float(cggz_js[cs][1]))/float(cggz_js[cs][1])*100#计算盈亏幅度
	zyke = (float(cggz_gpxx[1])-float(cggz_js[cs][1]))*float(cggz_js[cs][0])#计算总盈亏额
	jryk = float(cggz_gpxx[3])*float(cggz_js[cs][0])#计算今日盈亏
	riqi = time.strftime("%m/%d", time.localtime())
	cggz_gpxx.insert(1,cggz_js[cs][2])#插入持有数量
	cggz_gpxx.insert(2,cggz_js[cs][0])#插入持有数量
	cggz_gpxx.insert(3, cggz_js[cs][1])#插入持有成本
	cggz_gpxx.insert(4, str("%.0f" % jryk))# 插入今日盈亏
	cggz_gpxx.insert(5, str("%.2f" % ykfd)+'%')#插入盈亏幅度
	cggz_gpxx.insert(6, str("%.0f" % zyke))# 插入盈亏幅度
	cggz_gpxx.insert(9,cggz_js[cs][4])# 插入总盈亏额
	cggz_gpxx.insert(10,cggz_js[cs][3])# 插入卖出日期
	cggz_gpxx.append(hy_js[cs])
	cggz_zb[cs] = cggz_gpxx

cggz_df = pd.DataFrame(cggz_zb)

cggz_df.index = ['名称', '买入日期', '持有数量', '成本价', '今日盈亏', '盈亏幅度', '总盈亏', '当前价格','当前幅度','盈亏总额','卖出日期','当日涨跌','换手率','量比','流通市值','行业']
cggz_df = cggz_df.T
st.dataframe(cggz_df)

jrykze = 0
cggz_df = cggz_df[cggz_df['盈亏总额']== "-"]
for i in cggz_df['今日盈亏']:
	jrykze += float(i)


st.write(jrykze)
