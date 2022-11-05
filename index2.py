
# coding: utf-8
import pandas as pd
import json
import requests
import streamlit as st
import time

xq_list = ["周日","周一","周二","周三","周四","周五","周六"]
riqi = time.strftime("%m-%d-%H-%M", time.localtime())
xingqi = time.strftime("%w", time.localtime())
riqi = riqi + ":" + xq_list[int(xingqi)]

st.write(riqi)
