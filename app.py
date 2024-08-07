import streamlit as st
import pandas as pd
import time as ti
import re
from datetime import date,datetime,timedelta
from facebook_business.api import FacebookAdsApi 
from facebook_business.adobjects.adaccount import AdAccount 
from facebook_business.adobjects.ad import Ad 
from facebook_business.adobjects.campaign import Campaign 
from facebook_business.adobjects.adsinsights import AdsInsights 

def lock_fun():
    st.session_state.lock = True
    
def lock2_fun():
    st.session_state.lock2 = True 
    
def lock3_fun():
    st.session_state.lock3 = True 
    
def uuspa_meta_api_link():
    #顯示單日廣告表現細項
    def view_ad_detile(start_search_date,end_search_date):
        #細節存放容器
        detile_ad_num=[]
        detile_ad_name=[]
        detile_ad_spend=[]
        detile_ad_impressions=[]
        detile_ad_clicks=[]
        detile_ad_ctr=[]
        detile_ad_cpm=[]
        # 指定開始和結束時間（Unix 時間戳） 
        params = { 
            'time_range': { 
            'since': str(start_search_date),  # 替換為你想要的開始日期 
            'until': str(end_search_date)   # 替換為你想要的結束日期 
            }, 
            'fields': ['name','id']
        }
        # 獲取廣告集 
        ad_sets = my_account.get_ads(params=params) 
        #要顯示的欄位 
        meta_columns=['廣告ID','廣告名稱','花費金額','曝光次數','連結點擊次數','CTR(連結點閱率)','CPM(每千次廣告曝光成本)'] 
        #迭代每個廣告集並獲取廣告 
        for ad in ad_sets: 
            #避免過量讀取 
            #ti.sleep(1)
            ad_id = ad['id']  
            ad_name = ad['name'] 
            insights_params = { 
                'fields': [ 
                    AdsInsights.Field.reach, 
                    AdsInsights.Field.frequency, 
                    AdsInsights.Field.spend, 
                    AdsInsights.Field.impressions, 
                    AdsInsights.Field.cpm, 
                    AdsInsights.Field.ctr, 
                    AdsInsights.Field.clicks,
                ], 
                'time_range': { 
                    'since': str(start_search_date),  # 替換為你想要的開始日期 
                    'until': str(end_search_date)   # 替換為你想要的結束日期 
                } 
            } 
            insights = Ad(ad_id).get_insights(params=insights_params) 
            for insight in insights:

                ctr_cal=f'{float(insight["ctr"]):.2f}%' 
                cpm_cal=f'{float(insight["cpm"]):.2f}' 
                #各項廣告的細節依序存入容器
                detile_ad_num.append(ad_id)
                detile_ad_name.append(ad_name)
                detile_ad_spend.append(insight['spend'])
                detile_ad_impressions.append(insight['impressions'])
                detile_ad_clicks.append(insight['clicks'])
                detile_ad_ctr.append(ctr_cal)
                detile_ad_cpm.append(cpm_cal)

        ad_data_detile = {
            meta_columns[0]:detile_ad_num,
            meta_columns[1]:detile_ad_name,
            meta_columns[2]:detile_ad_spend,
            meta_columns[3]:detile_ad_impressions,
            meta_columns[4]:detile_ad_clicks,
            meta_columns[5]:detile_ad_ctr,
            meta_columns[6]:detile_ad_cpm
        }
        ad_data_all_detile=pd.DataFrame(ad_data_detile)
        ad_data_all_detile_view=st.dataframe(ad_data_all_detile)
    
    #每日    
    def single_view_ad(start_date,end_date):
        
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
        
        single_date=st.selectbox('請選擇日期',date_list)
        
        if single_date: 
            view_ad_detile(single_date,single_date)
    
    #每禮拜
    def view_ad(start_date,end_date):
        
        dates=pd.date_range(start_date,end_date) 
        week_date_list=[] 
        save_weeks=[] 
        current_weeks=[]
        
        for data_var in dates: 
            if data_var.weekday()==0 and current_weeks: 
                save_weeks.append(current_weeks)
                current_weeks=[]
            current_weeks.append(data_var)
            
        if current_weeks:
            save_weeks.append(current_weeks)
            
        for key,value in enumerate(save_weeks):
            week_date_list.append(f'Week {key+1}: {value[0].date()}~{value[-1].date()}') 
        
        for var in week_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
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
            
            # 轉為小數點第二位與百分比 
            ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
            cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            ctr_list.append(ctr_cal)
            cpm_list.append(cpm_cal)
            #存入每禮拜日期
            date_list.append(var) 
        
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
        single_date=st.selectbox('請選擇日期',date_list)
        if single_date:
           date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
           view_ad_detile(date_filter[0], date_filter[1])
    
    #每月
    def month_view_ad(start_date,end_date):
        
        dates = pd.date_range(start_date, end_date)
        month_date_list = []
        save_months = []
        current_months = []

        for data_var in dates:
            # 當月份改變時，將當前月的日期添加到 save_months，並重置 current_months
            if data_var.day == 1 and current_months:
                save_months.append(current_months)
                current_months = []
            current_months.append(data_var)

        # 將最後一個月的日期添加到 save_months
        if current_months:
            save_months.append(current_months)

        # 格式化每個月的日期範圍
        for key, value in enumerate(save_months):
            month_date_list.append(f'Month {key + 1}: {value[0].date()}~{value[-1].date()}')

        # 打印每個月的日期範圍
        for var in month_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
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
            
            # 轉為小數點第二位與百分比 
            ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
            cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            ctr_list.append(ctr_cal)
            cpm_list.append(cpm_cal)
            #存入每禮拜日期
            date_list.append(var) 
        
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
        single_date=st.selectbox('請選擇日期',date_list)
        if single_date:
            date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
            view_ad_detile(date_filter[0], date_filter[1])
    
    #uuspa_meta_api_link函式主程式
    my_app_id = '979970737212193' 
    my_app_secret = '10d42ab770d274dea7b7e7d3924d416b' 
    my_access_token = 'EAAN7RzeuiyEBOZCNhdkGhOk625oDA0Yat9NiwiISNRnLBFXPNItzchxREOBuGMpVBHssTGeSyFtdhgzlxAISPxRnoBRQdR2DYVvb3MAHl1rtWFFLUZCZAS2f0wL73qMZAaEJIhBlf9wxRMlLSKl9cQXtYoLZCWQNzw3HjCsEQ5BvlqSQyxS0MNnaTigsLKU1J7ZAmReYvZC' 
    # 初始化 Facebook 廣告 API 
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token) 
    # 指定你的廣告帳戶 ID 
    my_account = AdAccount('act_1316371069004495')
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
            single_view_ad(start_date,end_date)
            
        elif date_group=='月-週':
            view_ad(start_date,end_date)
        
        elif date_group=='年-月':
            month_view_ad(start_date, end_date)
    
def uupon_meta_api_link():
    
    #顯示單日廣告表現細項
    def view_ad_detile(start_search_date,end_search_date):
        #細節存放容器
        detile_ad_num=[]
        detile_ad_name=[]
        detile_ad_spend=[]
        detile_ad_impressions=[]
        detile_ad_clicks=[]
        detile_ad_ctr=[]
        detile_ad_cpm=[]
        # 指定開始和結束時間（Unix 時間戳） 
        params = { 
            'time_range': { 
            'since': str(start_search_date),  # 替換為你想要的開始日期 
            'until': str(end_search_date)   # 替換為你想要的結束日期 
            }, 
            'fields': ['name','id']
        }
        # 獲取廣告集 
        ad_sets = my_account.get_ads(params=params) 
        #要顯示的欄位 
        meta_columns=['廣告ID','廣告名稱','花費金額','曝光次數','連結點擊次數','CTR(連結點閱率)','CPM(每千次廣告曝光成本)'] 
        #迭代每個廣告集並獲取廣告 
        for ad in ad_sets: 
            #避免過量讀取 
            #ti.sleep(1)
            ad_id = ad['id']  
            ad_name = ad['name'] 
            insights_params = { 
                'fields': [ 
                    AdsInsights.Field.reach, 
                    AdsInsights.Field.frequency, 
                    AdsInsights.Field.spend, 
                    AdsInsights.Field.impressions, 
                    AdsInsights.Field.cpm, 
                    AdsInsights.Field.ctr, 
                    AdsInsights.Field.clicks,
                ], 
                'time_range': { 
                    'since': str(start_search_date),  # 替換為你想要的開始日期 
                    'until': str(end_search_date)   # 替換為你想要的結束日期 
                } 
            } 
            insights = Ad(ad_id).get_insights(params=insights_params) 
            for insight in insights:

                ctr_cal=f'{float(insight["ctr"]):.2f}%' 
                cpm_cal=f'{float(insight["cpm"]):.2f}' 
                #各項廣告的細節依序存入容器
                detile_ad_num.append(ad_id)
                detile_ad_name.append(ad_name)
                detile_ad_spend.append(insight['spend'])
                detile_ad_impressions.append(insight['impressions'])
                detile_ad_clicks.append(insight['clicks'])
                detile_ad_ctr.append(ctr_cal)
                detile_ad_cpm.append(cpm_cal)

        ad_data_detile = {
            meta_columns[0]:detile_ad_num,
            meta_columns[1]:detile_ad_name,
            meta_columns[2]:detile_ad_spend,
            meta_columns[3]:detile_ad_impressions,
            meta_columns[4]:detile_ad_clicks,
            meta_columns[5]:detile_ad_ctr,
            meta_columns[6]:detile_ad_cpm
        }
        ad_data_all_detile=pd.DataFrame(ad_data_detile)
        ad_data_all_detile_view=st.dataframe(ad_data_all_detile)
    
    #每日    
    def single_view_ad(start_date,end_date):
        
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
        
        single_date=st.selectbox('請選擇日期',date_list)
        
        if single_date: 
            view_ad_detile(single_date,single_date)
    
    #每禮拜
    def view_ad(start_date,end_date):
        
        dates=pd.date_range(start_date,end_date) 
        week_date_list=[] 
        save_weeks=[] 
        current_weeks=[]
        
        for data_var in dates: 
            if data_var.weekday()==0 and current_weeks: 
                save_weeks.append(current_weeks)
                current_weeks=[]
            current_weeks.append(data_var)
            
        if current_weeks:
            save_weeks.append(current_weeks)
            
        for key,value in enumerate(save_weeks):
            week_date_list.append(f'Week {key+1}: {value[0].date()}~{value[-1].date()}') 
        
        for var in week_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
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
            
            # 轉為小數點第二位與百分比 
            ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
            cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            ctr_list.append(ctr_cal)
            cpm_list.append(cpm_cal)
            #存入每禮拜日期
            date_list.append(var) 
        
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
        single_date=st.selectbox('請選擇日期',date_list)
        if single_date:
           date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
           view_ad_detile(date_filter[0], date_filter[1])
    
    #每月
    def month_view_ad(start_date,end_date):
        
        dates = pd.date_range(start_date, end_date)
        month_date_list = []
        save_months = []
        current_months = []

        for data_var in dates:
            # 當月份改變時，將當前月的日期添加到 save_months，並重置 current_months
            if data_var.day == 1 and current_months:
                save_months.append(current_months)
                current_months = []
            current_months.append(data_var)

        # 將最後一個月的日期添加到 save_months
        if current_months:
            save_months.append(current_months)

        # 格式化每個月的日期範圍
        for key, value in enumerate(save_months):
            month_date_list.append(f'Month {key + 1}: {value[0].date()}~{value[-1].date()}')

        # 打印每個月的日期範圍
        for var in month_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
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
            
            # 轉為小數點第二位與百分比 
            ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
            cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            ctr_list.append(ctr_cal)
            cpm_list.append(cpm_cal)
            #存入每禮拜日期
            date_list.append(var) 
        
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
        single_date=st.selectbox('請選擇日期',date_list)
        if single_date:
            date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
            view_ad_detile(date_filter[0], date_filter[1])
    
    #uupon_meta_api_link函式主程式
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
            single_view_ad(start_date,end_date)
            
        elif date_group=='月-週':
            view_ad(start_date,end_date)
        
        elif date_group=='年-月':
            month_view_ad(start_date, end_date)

            
    # elif ad_group=='行銷活動':
    
    # elif ad_group=='廣告組合':
    
    
    
    
if 'lock' not in st.session_state:
    st.session_state.lock =False
    st.session_state.lock2=False
    st.session_state.lock3=False

st.session_state["clicked"] = True


# 設定開頭文字
st.title("由上往下依序進行操作")
st.write("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    <p class="big-font">※溫馨小提示 : 為確保系統能正常執行，建議在操作上不要太過頻繁，看清楚選項再進行動作</p>
""", unsafe_allow_html=True)
st.write("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    <p class="big-font">⁂ 錯誤應對機制 : 先讓網頁休息5~10分鐘再進行作業</p>
""", unsafe_allow_html=True)
# 選擇廣告類別:UUPON、buty99
choose_ad_class=st.selectbox('請選擇廣告類別', ['UUPON','UUSPA(Buty99)'],disabled=st.session_state.lock,key='w1')
st.write('選擇廣告類別是：',choose_ad_class)

# 讓使用者選擇日期

start_date = st.date_input("請選擇起始日期",disabled=st.session_state.lock,key='w2')
end_date = st.date_input("請選擇結束日期",disabled=st.session_state.lock,key='w3')

# 顯示使用者選擇的日期

col1, col2 = st.columns(2)
with col1:
    st.write("您選擇的起始日期是：", start_date)
with col2:
    st.write("您選擇的結束日期是：", end_date)

adclass_date_sub=st.button('以上選擇確定',on_click=lock_fun,disabled=st.session_state.lock,key='w4')

if st.session_state.lock:
    st.session_state.lock=True
    if end_date<start_date:
        st.write("結束日期小於開始日期，請刷新網頁再重新選擇")
    else:
        # 選擇日期組合
        date_group=st.selectbox('請選擇日期組合', ['單日', '年-月', '月-週'],disabled=st.session_state.lock3,key='w5')
        # 顯示選中的選項
        st.write('您選擇的日期組合是：', date_group)
        
        # 選擇廣告平台
        if choose_ad_class=="UUPON":
            ad_platform=st.selectbox('請選擇廣告平台', ['Meta', 'GA4'],disabled=st.session_state.lock3,key='w7')
        elif choose_ad_class=="UUSPA(Buty99)":
            ad_platform=st.selectbox('請選擇廣告平台', ['Meta', 'GA4', 'Shopline'],disabled=st.session_state.lock3,key='w8')
        st.write('您選擇的平台是：', ad_platform)
        
        #選擇廣告群組類型
        ad_group=st.selectbox('請選擇廣告群組', ['廣告'],disabled=st.session_state.lock3,key='w6')
        # 顯示選中的選項
        st.write('您選擇的廣告群組是：', ad_group)
        view_ad_sub=st.button('查詢廣告數據',on_click=lock3_fun,disabled=st.session_state.lock3,key='w9')
        #依照選擇的平台來進行不同的API串接
        #切身之痛
        if st.session_state.lock3:
            if choose_ad_class=='UUPON':
                if ad_platform=='Meta':
                    uupon_meta_api_link()
                elif ad_platform=='GA4':
                    st.write("Python link GA4 API")
            elif choose_ad_class=='UUSPA(Buty99)':
                if ad_platform=='Meta':
                    uuspa_meta_api_link()
                elif ad_platform=='GA4':
                    st.write("UUSPA Python link GA4 API")
                elif ad_platform=='GA4':
                    st.write("UUSPA Python link GA4 API")
