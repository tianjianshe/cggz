
# coding: utf-8
import pandas as pd
import json
import requests
import streamlit as st
import time

#大盘最新价格
df_cy = pd.DataFrame()
df_cy = ak.stock_zh_a_spot_em()
#先获取当前日期，格式8-29：周一
xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
riqi = time.strftime("%m-%d-%H-%M", time.localtime())
xingqi = time.strftime("%w", time.localtime())
riqi = riqi + ":" + xq_list[int(xingqi)]

st.write(riqi)