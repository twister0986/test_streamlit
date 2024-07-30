import streamlit as st
import pandas as pd


 
# 設定標題
st.title("由上往下依序進行操作")

# 讓使用者選擇日期

start_date = st.date_input("請選擇起始日期")
end_date = st.date_input("請選擇結束日期")

# 顯示使用者選擇的日期

col1, col2 = st.columns(2)
with col1:
    st.write("您選擇的起始日期是：", start_date)
with col2:
    st.write("您選擇的結束日期是：", end_date)


if st.button('按我'):
    st.write('你按下了按鈕！')
    
# 建立選項列表
options = ['蘋果', '香蕉', '橘子']

# 建立下拉式選單
selected_option = st.selectbox('請選擇水果', options)

# 顯示選中的選項
st.write('您選擇的水果是：', selected_option)


# 樣本資料 (可以替換成你的資料)
data = [
    {'name': '節點1',
     'children': [
         {'name': '子節點11', 'data': [{'column1': 'value1', 'column2': 'value2'}]},
         {'name': '子節點12', 'data': [{'column1': 'value3', 'column2': 'value4'}]}
     ]},
    {'name': '節點2',
     'data': [{'column1': 'value5', 'column2': 'value6'}]}
]


st.dataframe(data)
