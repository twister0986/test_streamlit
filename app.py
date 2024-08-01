import streamlit as st
import pandas as pd
from datetime import timedelta
from facebook_business.api import FacebookAdsApi 
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights 

def lock_fun():
    st.session_state.lock = True
    
def lock2_fun():
    st.session_state.lock2 = True 
    
def lock3_fun():
    st.session_state.lock3 = True 
    
def uupon_meta_api_link():
    
    
    
    my_app_id = '762664479369512' 
    my_app_secret = '7122b271254c71d3303909eedd6ef938' 
    my_access_token = 'EAAK1o6lgKSgBO4sYE3u0s0GtTgPr0m83KDYyrWeQ1zXNVjETra57Hc6vmSAyXFBFWEJxM20dk9aXvnhGHidb6WFpzXF1OdZCZAbRhN5ZCvfzZCP2iVVQ2KmHH8XxOLDvX9mq3z6oa115gLocXnZAOW3DlgYqyfGZCOdazhYmerLquP3xtMKCHssD0hZAsCPZCooMchsZCcSiH' 
    # 初始化 Facebook 廣告 API 
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token) 
    # 指定你的廣告帳戶 ID 
    my_account = AdAccount('act_1033945910984802') 
    #要顯示的欄位 
    meta_columns=['日期','花費金額','曝光次數','點擊次數(全部)','CTR(連結點閱率)','CPM(每千次廣告曝光成本)'] 
    #儲存結果的容器
    date_list=[]
    spend_list=[]
    impressions_list=[]
    clicks_list=[]
    ctr_list=[]
    cpm_list=[]
    
    if ad_group=='廣告':
        if date_group=='單日':
            cal_start_var=start_date
            cal_end_var=end_date
            while True:
                # 判斷日期是否相等機制
                # 指定日期範圍 
                time_range = {
                    'since': str(cal_start_var),  # 替換為你想要的開始日期 
                    'until': str(cal_start_var)   # 替換為你想要的結束日期 
                }
                # 查詢廣告層級的統計數據 
                params = { 
                    'time_range': time_range, 
                    'fields': [ 
                        AdsInsights.Field.spend,  # 花費金額 
                        AdsInsights.Field.impressions,  # 曝光次數 
                        AdsInsights.Field.clicks,  # 總點擊次數 
                        AdsInsights.Field.ctr, # CTR(連結點閱率) 
                        AdsInsights.Field.cpm, # CPM(每千次廣告曝光成本) 
                    ], 
                }
                # 獲取帳戶層級的統計數據 
                insights = my_account.get_insights(params=params) 
    
                if len(insights) == 0: 
                    cal_start_var+=timedelta(days=1) 
                    if cal_start_var==cal_end_var: 
                        break
                    continue 
    
                # 轉為小數點第二位與百分比 
                ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                #存入容器
                spend_list.append(insights[0]['spend'])
                impressions_list.append(insights[0]['impressions'])
                clicks_list.append(insights[0]['clicks'])
                ctr_list.append(ctr_cal)
                cpm_list.append(cpm_cal)
                #存入每日日期
                date_list.append(cal_start_var)
                
                if cal_start_var==cal_end_var: 
                    break
                cal_start_var+=timedelta(days=1)
            
            
            #結果整理成dataframe
            
            ad_data = {
                meta_columns[0]:date_list,
                meta_columns[1]:spend_list,
                meta_columns[2]:impressions_list,
                meta_columns[3]:clicks_list,
                meta_columns[4]:ctr_list,
                meta_columns[5]:cpm_list,
            }
            ad_data_all=pd.DataFrame(ad_data)
            ad_data_all_view=st.dataframe(ad_data_all)

            st.selectbox('請選擇日期',[1,2,3,4,5],key='nodis')
            

     

            
            
            
            
            
            
            
            
            
    # elif ad_group=='行銷活動':
    
    # elif ad_group=='廣告組合':
    
    
    
    
if 'lock' not in st.session_state:
    st.session_state.lock =False
    st.session_state.lock2=False
    st.session_state.lock3=False

st.session_state["clicked"] = True


# 設定開頭文字
st.title("由上往下依序進行操作")
# 選擇廣告類別:UUPON、buty99
choose_ad_class=st.selectbox('請選擇廣告類別', ['UUPON','UUSPA(Buty99)'],disabled=st.session_state.lock)
st.write('選擇廣告類別是：',choose_ad_class)

# 讓使用者選擇日期

start_date = st.date_input("請選擇起始日期",disabled=st.session_state.lock)
end_date = st.date_input("請選擇結束日期",disabled=st.session_state.lock)

# 顯示使用者選擇的日期

col1, col2 = st.columns(2)
with col1:
    st.write("您選擇的起始日期是：", start_date)
with col2:
    st.write("您選擇的結束日期是：", end_date)

adclass_date_sub=st.button('以上選擇確定',on_click=lock_fun,disabled=st.session_state.lock)

if st.session_state.lock:
    if end_date<start_date:
        st.write("結束日期小於開始日期，請刷新網頁再重新選擇")
    else:
        # 選擇日期組合
        date_group=st.selectbox('請選擇日期組合', ['單日', '年-月', '月-週'],disabled=st.session_state.lock3)
        # 顯示選中的選項
        st.write('您選擇的日期組合是：', date_group)
        #選擇廣告群組類型
        ad_group=st.selectbox('請選擇廣告群組', ['行銷活動', '廣告組合', '廣告'],disabled=st.session_state.lock3)
        # 顯示選中的選項
        st.write('您選擇的廣告群組是：', ad_group)
        # 選擇廣告平台
        if choose_ad_class=="UUPON":
            ad_platform=st.selectbox('請選擇廣告平台', ['Meta', 'GA4'],disabled=st.session_state.lock3)
        elif choose_ad_class=="UUSPA(Buty99)":
            ad_platform=st.selectbox('請選擇廣告平台', ['Meta', 'GA4', 'Shopline'],disabled=st.session_state.lock3)
        st.write('您選擇的平台是：', ad_platform)
        view_ad_sub=st.button('查詢廣告數據',on_click=lock3_fun,disabled=st.session_state.lock3)
        #依照選擇的平台來進行不同的API串接
        if view_ad_sub:
            if ad_platform=='Meta':
                
                uupon_meta_api_link()
                
            elif ad_platform=='GA4':
                st.write("Python link GA4 API")
