
# coding: utf-8
import pandas as pd
import json
import requests
import streamlit as st
import time

cggz_file = "./cggz.json"#连接JSON数据库文件：【持股跟踪】
with open(cggz_file) as f5:
	cggz_js = json.load(f5)#读取JSON文件的信息，转化为字典,获取【持股跟踪】写入的基本信息



#先获取当前日期，格式8-29：周一
xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
riqi = time.strftime("%m-%d-%H-%M", time.localtime())
xingqi = time.strftime("%w", time.localtime())
riqi = riqi + ":" + xq_list[int(xingqi)]

st.write(riqi)
st.write(cggz_js)