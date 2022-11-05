import akshare as ak
import pandas as pd
import json
import heapq
import time
from apscheduler.schedulers.blocking import BlockingScheduler

shuchu3_list= []
def stock_job():
	#先获取当前日期，格式8-29：周一	
	xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
	riqi = time.strftime("%y%m%d", time.localtime())
	xingqi = time.strftime("%w", time.localtime())
	shijian = time.strftime("%H:%M", time.localtime())
	xiaoshi = time.strftime("%H", time.localtime())
	if xingqi != "6" and xingqi != "0":
		hangye_file = "./data/hangye.json"#连接JSON数据库文件：大盘压力位和支撑位记录
		with open(hangye_file) as f5:
			hy_js = json.load(f5)#读取JSON文件的信息，转化为字典

		df = pd.DataFrame()

		df = ak.stock_zh_a_spot_em()

		gp_zt = df[df['涨跌幅']>9.9]#涨停股票
		gp_zt_dm = gp_zt['代码']

		gp_dt = df[df['涨跌幅']<-9.9]#跌停股票
		gp_dt_dm = gp_dt['代码']

		hysl_list = [] #涨停行业数量list
		for i in gp_zt_dm:
			y = hy_js.get(i)
			hysl_list.append(y)
		ztsl=len(hysl_list)#涨停数量

		dtsl=len(gp_dt)#跌停数量
		hymc = list(set(hysl_list))#删除重复项

		if None in hymc:
			hymc.remove(None)

		hysl = []
		for i in hymc:
			hysl.append(hysl_list.count(i))

		data = [hymc,hysl]

		df1 = pd.DataFrame(data)
		df1.index = ["行业","数量"]
		df2 = df1.T
		df2.sort_values(by="数量" , inplace=True, ascending=False) 
		df3 = df2.head()
		shuchu_list = []

		y = df3["行业"]
		for i in y:
			shuchu_list.append(i)
		z=0
		shuchu2_list = []
		y = df3['数量']
		for i in y:
			shuchu2_list.append(shuchu_list[z]+str(i))
			z +=1

		wendu = ztsl/(ztsl+dtsl)*100
		wendu = str("%.1f" % wendu)+'℃'

		shuchu3_list = [shijian,ztsl,dtsl,wendu]
		shuchu3_list = shuchu3_list+shuchu2_list
		shuchu4_list = [str(ztsl),str(dtsl),wendu]
		shuchu4_list = shuchu4_list+shuchu2_list

		ztbktj_file = "./data/ztbktj.json"#连接JSON数据库文件：涨停板块统计
		with open(ztbktj_file) as f5:
			ztbktj_js = json.load(f5)#读取JSON文件的信息，转化为字典
		ny = riqi in ztbktj_js
		shujudiejia = [] #与前日数据叠加

		if ny == False:
			ztbktj_js[riqi] = shuchu3_list
		else:
			if type(ztbktj_js[riqi][0]) == str:
				shujudiejia.append(ztbktj_js[riqi])
				shujudiejia.append(shuchu3_list)
				ztbktj_js[riqi] = shujudiejia
			else:
				shujudiejia = ztbktj_js[riqi]
				shujudiejia.append(shuchu3_list)
				ztbktj_js[riqi] = shujudiejia

		with open(ztbktj_file, "w") as f2:
			json.dump(ztbktj_js, f2)

		print(shijian,"成功写入数据")

		if xiaoshi == "15" and xingqi != "6" and xingqi != "0":
			lszdttj_file = "./data/lszdttj.json"#连接JSON数据库文件：大盘压力位和支撑位记录
			with open(lszdttj_file) as f8:
				lszdt_js = json.load(f8)#读取JSON文件的信息，转化为字典
			lszdt_js[riqi] = shuchu4_list
			with open(lszdttj_file, "w") as f9:
				json.dump(lszdt_js, f9)
	else:
		print(shijian,"今天是非交易日……")

#stock_job()#直接启动革命工作

if __name__ == '__main__':
    sched = BlockingScheduler()
    # 每天10:00、10:30、11:00、12:00、13:30、14:00、14:30、15:30 执行
    sched.add_job(stock_job, 'cron', hour=9, minute=30)
    sched.add_job(stock_job, 'cron', hour=10, minute=00)
    sched.add_job(stock_job, 'cron', hour=10, minute=30)
    sched.add_job(stock_job, 'cron', hour=11, minute=00)
    sched.add_job(stock_job, 'cron', hour=12, minute=00)
    sched.add_job(stock_job, 'cron', hour=13, minute=30)
    sched.add_job(stock_job, 'cron', hour=14, minute=00)
    sched.add_job(stock_job, 'cron', hour=14, minute=30)
    sched.add_job(stock_job, 'cron', hour=15, minute=1)
    sched.start()