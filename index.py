
# coding: utf-8
import pandas as pd
import json
import requests
import streamlit as st
import time
import akshare as ak
st.set_page_config(
    page_title="格GU致知",    #页面标题
    page_icon=":anger:",        #icon
    layout="centered",                #页面布局
    initial_sidebar_state="auto"  #侧边栏
)


#大盘最新价格
dp_df = pd.DataFrame()
dp_df = ak.stock_zh_index_spot()
dp_zxj = dp_df["最新价"][0]
dp_zdf = dp_df["涨跌幅"][0]
#先获取当前日期，格式8-29：周一
xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
riqi = time.strftime("%m-%d-%H-%M", time.localtime())
xingqi = time.strftime("%w", time.localtime())
riqi = riqi + ":" + xq_list[int(xingqi)]

hangye_file = "./data/hangye.json"#连接JSON数据库文件：个股行业查询
with open(hangye_file) as f5:
	hy_js = json.load(f5)#读取JSON文件的信息，转化为字典

hysl_file = "./data/hysl.json"#连接JSON数据库文件：行业数量
with open(hysl_file) as f5:
	hysl_js = json.load(f5)#读取JSON文件的信息，转化为字典

riji_file = "./data/riji.json"#连接JSON数据库文件：日记的数据
with open(riji_file) as f2:
	rj_js = json.load(f2)#读取JSON文件的信息，转化为字典
rj_list = []
for x, y in reversed(rj_js.items()):
	rj_list.append(x)
gpxx_df = pd.DataFrame() #建立整个股票信息的DataFrame
#----------------------------------侧边栏-------------------------------------------------------
st.sidebar.image("./material/tubiao.png")

st.sidebar.markdown("#### 功能栏")
dapan_file = "./data/dapan.json"#连接JSON数据库文件：大盘压力位和支撑位记录
with open(dapan_file) as f1:
	dp_js = json.load(f1)#读取JSON文件的信息，转化为字典

with st.sidebar.expander("大盘压力情况"):#.sidebar是侧边栏，.expander是折叠窗口

	with st.form(key='my_form2'):
		dpzcw = st.text_input('压力位')  #变量名的意思是：大盘支撑位
		dpylw = st.text_input('支撑位')  #变量名的意思是：大盘压力位

		submdapit_button = st.form_submit_button(label='提交')
		if dpylw != "":
			with open(dapan_file, "w") as f1:
				dp_js = [dpzcw,dpylw]
				json.dump(dp_js, f1)

#以下是利用streamlit添加新的有缺口的股票---------------------------------------

jsonfile = "./data/gupiao.json"#连接JSON数据库文件：股票代码+缺口上端+缺口下端
with open(jsonfile) as f:
	js_gp = json.load(f)#读取JSON文件的信息，转化为字典

with st.sidebar.expander("缺口-添加股票"):
	with st.form(key='my_form'):
		gpdm_tj = st.text_input('股票代码')  #变量名的意思是：股票代码_添加
		qkxd_tj = st.text_input('缺口下端')  #变量名的意思是：缺口下端_添加
		qksd_tj = st.text_input('缺口上端')  #变量名的意思是：缺口上端_添加
		submit_button = st.form_submit_button(label='提交')
		if gpdm_tj != "":
			with open(jsonfile, "w") as f:
				js_gp[gpdm_tj] = [qkxd_tj,qksd_tj]
				json.dump(js_gp, f)

#添加新的有缺口的股票功能结束--------------------------------------------------


#以下是利用streamlit删除股票-------------------------------------------------
with st.sidebar.expander("缺口-删除股票"):

	with st.form(key='my_form1'):
		gpdm_sc = st.text_input('股票代码')  #变量名的意思是：股票代码_删除
		submit_button = st.form_submit_button(label='删除')
		if gpdm_sc != "":
			del js_gp[str(gpdm_sc)]
			with open(jsonfile, "w") as f:
				json.dump(js_gp, f)
			gpdm_sc = ""

#以下是测算两个价格之间的百分比距离-------------------------------------------------
with st.sidebar.expander("测算百分比距离"):

	with st.form(key='my_form3'):
		jg1_jz = st.text_input('价格1(基准)')  #变量名的意思是：价格1_基准
		jg2 = st.text_input('价格2')  # 变量名的意思是：价格2
		submit_button = st.form_submit_button(label='测算')
		if jg1_jz != "":
			juli = (float(jg1_jz)-float(jg2))/float(jg1_jz)*100
			st.write(str("%.1f" % juli)+'%')
			jg1_jz = ""

#以下是添加新股行业的模块-------------------------------------------------
with st.sidebar.expander("添加新股行业"):#.sidebar是侧边栏，.expander是折叠窗口

	with st.form(key='my_form6'):
		xgdm = st.text_input('新股代码')  #变量名的意思是：新股代码
		xghy = st.text_input('新股行业')  #变量名的意思是：新股行业

		submdapit_button = st.form_submit_button(label='提交')
		st.markdown('###### *本功能与行业个股数量关联')
		if xgdm != "":
			with open(hangye_file, "w") as f6:
				hy_js[xgdm] = xghy
				json.dump(hy_js, f6)

			with open(hysl_file, "w") as f7:
				q = hysl_js[xghy]
				hysl_js[xghy] = q + 1
				json.dump(hysl_js, f7)

#以下是查询行业中个股数量的模块-------------------------------------------------

with st.sidebar.expander("查询行业个股数量"):#.sidebar是侧边栏，.expander是折叠窗口
	with st.form(key='my_form8'):
		hymc = st.text_input('输入行业名称')  #变量名的意思是：新股代码
		submdapit_button = st.form_submit_button(label='查询')
		if hymc in hysl_js:
			st.write(hysl_js[hymc])


# 以下是利用streamlit删除股票-------------------------------------------------
with st.sidebar.expander("删除日记"):

	with st.form(key='my_form7'):
		riji_sc = st.text_input('你要删除第几条？')  # 变量名的意思是：股票代码_删除
		submit_button = st.form_submit_button(label='删除')
		if riji_sc != "":
			i = int(riji_sc)-1

			del rj_js[rj_list[i]]
			with open(riji_file, "w") as f8:
				json.dump(rj_js, f8)
			riji_sc = None
#----------------------------------中间主体-------------------------------------------------------

#开始书写大盘的压力位和支撑位-------------------------------------------------


col1, col2, col3,col4= st.columns(4)
with col1:
	st.metric("大盘指数", "%.1f" % dp_zxj)

with col2:
	st.metric("大盘涨幅", str("%.2f" % dp_zdf)+'%')

with col3:
	ylwjl = float(dp_zxj)-float(dp_js[0])
	st.metric("大盘压力位", dp_js[0],"%.1f" % ylwjl)

with col4:
	zcwjl = float(dp_zxj) - float(dp_js[1])
	st.metric("大盘支撑位", dp_js[1],"%.1f" % zcwjl)


st.markdown("---")#画一条水平线

#开始读取json数据库中的股票的信息-------------------------------------------------

col7,col8 =st.columns(2)
with col7:
	st.markdown("##### 股票缺口实时观测表")
with col8:
	st.button('刷新')

def time_printer():#股票信息显示函数
	gpxx_hz = {} #创建所有股票的汇总数据字典
	for gpdm in js_gp:
		url = 'https://hqm.stock.sohu.com/getqjson?code=cn_'+gpdm
		req = requests.get(url,timeout=30) # 请求连接
		req = req.content #返回二进制数据
		req = req.decode('gb2312')  #转换编码
		#以下三行是获取字符串中的“[]”间的数据，其他数据不要
		nPos=req.index("[")
		nPos1=req.index("]")
		req = req[nPos:nPos1+1]
		req_list = json.loads(req) #将字符串转化为json格式的数据
		xulie = (1,2,3,8,11,16)#需要获取req_list中的元组中6个位置的数据：股票名称、当前价、当日涨幅、换手率、最低价、流通股市值
		gpxx = []  # 创建股票信息列表，存储单个股票以上6个需要数据
		for i in xulie:
			gpxx.append(req_list[i])
		#以下代码判断股票缺口是否已经消失和计算缺口距离-----------------------------------------------
		dqjg = float(gpxx[1]) #当前价格变量--------将字符串转化为浮点数
		zdjg = float(gpxx[4]) #当日最低价格
		qkxd = float(js_gp[gpdm][0]) #缺口下端价格
		qksd = float(js_gp[gpdm][1]) #缺口上端价格

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

	#开始读取json数据库中的股票的信息,呈现涨停板块统计---------------------------------------
	with st.expander("今日涨跌停情况统计"):
		riqi1 = time.strftime("%y%m%d", time.localtime())
		ztbktj_file = "./data/ztbktj.json"#连接JSON数据库文件：涨停板块统计
		with open(ztbktj_file) as f10:
			ztbktj_js = json.load(f10)#读取JSON文件的信息，转化为字典
		ny = riqi1 in ztbktj_js
		if xingqi != "6" and xingqi != "0":
			if ny == True:
				yy = ztbktj_js[riqi1]
				ztbktj_df = pd.DataFrame(yy)#,index = ["时间","涨停数","跌停数","温度","行业1","行业2","行业3","行业4","行业5"])
				#ztbktj_df =ztbktj_df.T
				ztbktj_df.columns = ["时间","涨停数","跌停数","温度","行业1","行业2","行业3","行业4","行业5"]
				st.write(ztbktj_df)
			else:
				st.write("9:30以后更新……")
		else:
			st.write("今天是非交易日……")

	with st.expander("历史涨跌停情况统计"):

		lsztbktj_file = "./data/lszdttj.json"#连接JSON数据库文件：涨停板块统计
		with open(lsztbktj_file) as f11:
			lsztbktj_js = json.load(f11)#读取JSON文件的信息，转化为字典

			lsztbktj_df = pd.DataFrame(lsztbktj_js,index = ["涨停数","跌停数","温度","行业1","行业2","行业3","行业4","行业5"])

			st.dataframe(lsztbktj_df.iloc[:, ::-1])#让后面的列排到前面，倒序出现→.iloc[:, ::-1]

def riji_printer():#日记本函数

	with st.expander("新建日记"):
		with st.form(key='my_form4'):
			xjrj = st.text_area("")
			submdapit_button = st.form_submit_button(label='提交')
			if xjrj != "":
				with open(riji_file, "w") as f2:
					rj_js[riqi] = xjrj
					json.dump(rj_js, f2)
					st.success('日记保存成功!')
				xjrj = ""
	riji_show = st.sidebar.slider('日记显示条数')

	if riji_show == 0:
		riji_show = 8

	with st.expander("查看日记"):
		i = 0
		for x, y in reversed(rj_js.items()):
			col1, col2 = st.columns(2)
			with col1:
				st.markdown(x)
			with col2:
				riji_shu = "第"+str(i+1)+"条"
				st.markdown(riji_shu)
			st.markdown(y)
			st.markdown("---")
			i = i+1
			if i == riji_show:
				break
	st.markdown("---")#画一条水平线
	st.write("1→2→3→5→8→13→21→34→55→89→144→233")#画一条水平线
time_printer()
riji_printer()
