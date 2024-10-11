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
        #
        detile_ad_reach=[]
        detile_ad_spend=[]
        detile_ad_impressions=[]
        detile_ad_acr=[]
        detile_ad_ctr_link=[]
        detile_ad_ctr=[]
        detile_ad_cpm=[]
        detile_ad_cart=[]
        detile_ad_pay_num=[]
        detile_ad_link_clicks=[]
        detile_ad_cvr=[]
        detile_ad_roas=[]
        detile_ad_result_cost=[]
        detile_ad_buy_trans=[]
        #新增連結頁面瀏覽結果
        detile_ad_link_page_view=[]
        
        # 指定開始和結束時間（Unix 時間戳） 
        params = { 
            'time_range': { 
            'since': str(start_search_date),  # 替換為你想要的開始日期 
            'until': str(end_search_date)   # 替換為你想要的結束日期 
            }, 
            'fields': ['name','id']
        }
        # 獲取廣告集 
        my_app_id2 = '1497667584443557'
        my_app_secret2 = 'bcd21030e69b10b8c1576f2739dd3873'
        my_access_token2 = 'EAAVSHuhcxKUBOxNuwKnbf6eoyOg60v47byEP56qaYy3NBLR9dDrI7VpOE27LOSx8EHBfpGhKHAhXxuZCXBH71YALK5rn8hqMcFeMIaJ8kfd8GnYxhsDUFYug9emxXNXBDZBf25eTvjUUxq0ZB2WCnYupRvwmbPIdvFYR1ZBzEZBLAW8G62FjST5GW1KKOoyIldxGRQAZB8'
        # 初始化 Facebook 廣告 API 
        FacebookAdsApi.init(my_app_id2, my_app_secret2, my_access_token2) 
        # 指定你的廣告帳戶 ID 
        my_account2 = AdAccount('act_1316371069004495')
        ad_sets = my_account2.get_ads(params=params)
        
        #要顯示的欄位 
        #meta_columns=['廣告ID','廣告名稱','FB-加入購物車率','花費金額','FB-曝光次數','FB-點擊','FB-CTR(連結點閱率)','FB-平均客單價','FB-CPM(每千次廣告曝光成本)','FB-加入購物車','FB-訂單數','FB-CVR轉換率','FB-ROAS','FB-CPA','FB-轉換價值'] 
        #調整次數
        meta_columns=['廣告ID','廣告名稱','花費金額','FB-曝光次數','FB-點擊','FB-CTR(連結點閱率)','FB-加入購物車','FB-加入購物車率','FB-CPM(每千次廣告曝光成本)','FB-CPA','FB-訂單數','FB-CVR轉換率','FB-ROAS','FB-轉換價值','FB-平均客單價',] 
        
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
                    #AdsInsights.Field.conversions,
                    AdsInsights.Field.actions,
                    AdsInsights.Field.purchase_roas,
                    AdsInsights.Field.action_values,
                    AdsInsights.Field.cost_per_action_type,
                ], 
                'time_range': { 
                    'since': str(start_search_date),  # 替換為你想要的開始日期 
                    'until': str(end_search_date)   # 替換為你想要的結束日期 
                } 
            } 
            insights = Ad(ad_id).get_insights(params=insights_params) 
            #print(insights)
            for insight in insights:
                #活動數據路徑
                actions_path=insight['actions']
                #CPA路徑
                try:
                    cost_actions_path=insight['cost_per_action_type']
                except:
                    cost_actions_path=None
                #購買轉換值路徑
                try:
                    buy_trans_path=insight['action_values']
                except:
                    buy_trans_path=None
                save_index=0
                #購買轉換值
                try:
                    detile_ad_buy_trans_data = [trans['value'] for trans in buy_trans_path if trans['action_type'] == 'onsite_web_app_purchase']
                
                    #print(detile_ad_buy_trans_data)
                    detile_ad_buy_trans.append(detile_ad_buy_trans_data[0])
                except:
                    detile_ad_buy_trans.append('None')
                #每次成果成本
                try:
                    detile_ad_result_cost_data = [trans['value'] for trans in cost_actions_path if trans['action_type'] == 'web_in_store_purchase']
                
                    detile_ad_result_cost.append(detile_ad_result_cost_data[0])
                except:
                    detile_ad_result_cost.append('None')
                
                #取得 roas
                try:
                    detile_ad_roas_data=insight['purchase_roas'][0]['value']
                    detile_ad_roas_data=f'{float(detile_ad_roas_data):.2f}' 
                    detile_ad_roas.append(detile_ad_roas_data)
                except:
                    detile_ad_roas.append('None')
                
                #取得連結點擊次數
                for var in range(len(actions_path)):
                    if actions_path[var]['action_type']=='link_click':
                        detile_ad_link_clicks.append(actions_path[var]['value'])
                        save_index=var
                        break
                if save_index==0:
                    detile_ad_link_clicks.append('None')
                save_index=0
                #取得購買次數
                for var in range(len(actions_path)):
                    if actions_path[var]['action_type']=='purchase':
                        detile_ad_pay_num.append(actions_path[var]['value'])
                        save_index=var
                        break
                if save_index==0:
                    detile_ad_pay_num.append('None')
                save_index=0
                #計算 CVR 公式:購買次數÷連結點擊次數
                try:
                    detile_ad_cvr.append(f'{int(detile_ad_pay_num[-1])/int(detile_ad_link_clicks[-1])*100:.2f}%')
                except:
                    detile_ad_cvr.append('None')    
                #轉為小數點第二位與百分比
                #CTR(全部)，
                #改為FB-平均客單價，公式:購買轉換值÷購買次數
                try:
                    detile_ad_ctr_cal=f'{float(detile_ad_buy_trans[-1])/float(detile_ad_pay_num[-1]):.2f}'
                    detile_ad_ctr.append(detile_ad_ctr_cal)
                except:
                    detile_ad_ctr.append('None')
                #CPM    
                try:
                    cpm_cal=f'{float(insight["cpm"]):.2f}' 
                    detile_ad_cpm.append(cpm_cal)
                except:
                    detile_ad_cpm.append('None')
                #抽取加入購物車選項及存入容器
                
                for var in range(len(actions_path)):
                    if actions_path[var]['action_type']=='add_to_cart':
                        detile_ad_cart.append(actions_path[var]['value'])
                        save_index=var
                        
                        break
                if save_index==0:
                    detile_ad_cart.append('None')
                save_index=0
    
                #存入容器
                #各項廣告的細節依序存入容器
                detile_ad_num.append(ad_id)
                detile_ad_name.append(ad_name)
                #加入觸及人數
                #改為加入購物車率ACR
                for var in range(len(actions_path)):
                    if actions_path[var]['action_type']=='landing_page_view':
                        detile_ad_link_page_view.append(actions_path[var]['value'])
                        save_index=var
                        break
                if save_index==0:
                    detile_ad_link_page_view.append('None')
                save_index=0
                
                try:
                    acr_cal=f'{float(detile_ad_cart[-1])/float(detile_ad_link_page_view[-1])*100:.2f}%'
                    detile_ad_acr.append(acr_cal)
                except:
                    detile_ad_acr.append('None')
                    
                #
                try:
                    detile_ad_spend.append(insight['spend'])
                except:
                    detile_ad_spend.append('None')
                # 
                try:    
                    detile_ad_impressions.append(insight['impressions'])
                except:
                    detile_ad_impressions.append('None')
                #CTR(連結點閱率)
                try:
                    detile_ad_ctr_link_cal=f'{(float(detile_ad_link_clicks[-1])/float(detile_ad_impressions[-1])*100):.2f}%' 
                    detile_ad_ctr_link.append(detile_ad_ctr_link_cal)
                except:
                    detile_ad_ctr_link.append('None')
                    
        # ad_data_detile = {
        #     meta_columns[0]:detile_ad_num,
        #     meta_columns[1]:detile_ad_name,
        #     meta_columns[2]:detile_ad_acr,
        #     meta_columns[3]:detile_ad_spend,
        #     meta_columns[4]:detile_ad_impressions,
        #     meta_columns[5]:detile_ad_link_clicks,
        #     meta_columns[6]:detile_ad_ctr_link,
        #     meta_columns[7]:detile_ad_ctr,
        #     meta_columns[8]:detile_ad_cpm,
        #     meta_columns[9]:detile_ad_cart,
        #     meta_columns[10]:detile_ad_pay_num,
        #     meta_columns[11]:detile_ad_cvr,
        #     meta_columns[12]:detile_ad_roas,
        #     meta_columns[13]:detile_ad_result_cost,
        #     meta_columns[14]:detile_ad_buy_trans,
            
        # }
        
        ad_data_detile = {
            meta_columns[0]:detile_ad_num,
            meta_columns[1]:detile_ad_name,
            
            meta_columns[2]:detile_ad_spend,
            meta_columns[3]:detile_ad_impressions,
            meta_columns[4]:detile_ad_link_clicks,
            meta_columns[5]:detile_ad_ctr_link,
            meta_columns[6]:detile_ad_cart,
            meta_columns[7]:detile_ad_acr,
            meta_columns[8]:detile_ad_cpm,
            meta_columns[9]:detile_ad_result_cost,
            meta_columns[10]:detile_ad_pay_num,
            meta_columns[11]:detile_ad_cvr,
            meta_columns[12]:detile_ad_roas,
            meta_columns[13]:detile_ad_buy_trans,
            meta_columns[14]:detile_ad_ctr,
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
                    AdsInsights.Field.reach,#觸及人數
                    AdsInsights.Field.spend,  # 花費金額 
                    AdsInsights.Field.impressions,  # 曝光次數 
                    AdsInsights.Field.clicks,  # 總點擊次數 
                    AdsInsights.Field.ctr, # CTR(連結點閱率) 
                    AdsInsights.Field.cpm, # CPM(每千次廣告曝光成本) 
                    AdsInsights.Field.actions,#部分數據在活動
                    #AdsInsights.Field.conversions,
                    AdsInsights.Field.purchase_roas,
                    AdsInsights.Field.action_values,
                    AdsInsights.Field.cost_per_action_type,
                ], 
            }
            #獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params) 
            # print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            # print(insights)
            #購買轉換值:1580 purchase
            #[0]['cost_per_action_type'][0]['action_type]=='purchase'
            #"value": "2038"
            #purchase_roas[0]['value']:.2f
            #活動數據路徑
            #print(insights)
            try:
                actions_path=insights[0]['actions']
            except:
                actions_path=[]
            #CPA路徑
            try:
                cost_actions_path=insights[0]['cost_per_action_type']
            except:
                cost_actions_path=[]
            #購買轉換值路徑
            try:
                buy_trans_path=insights[0]['action_values']
            except:
                buy_trans_path=[]
            # if len(insights) == 0: 
            #     cal_start_var+=timedelta(days=1) 
            #     if cal_start_var==cal_end_var: 
            #         break
            #     continue 

            #以下各項如果沒有數據就放入 None
            #儲存索引值，用於判斷以下容器 list 是否放入 None
            
            save_index=0
            #購買轉換值
            buy_trans_data = [trans['value'] for trans in buy_trans_path if trans['action_type'] == 'onsite_web_app_purchase']
            try:
                buy_trans_list.append(buy_trans_data[0])
            except:
                buy_trans_list.append('None')
            #每次成果成本
            result_cost_data = [trans['value'] for trans in cost_actions_path if trans['action_type'] == 'web_in_store_purchase']
            try:
                result_cost_list.append(result_cost_data[0])
            except:
                result_cost_list.append('None')
            
            #取得 roas 
            try:
                roas_data=insights[0]['purchase_roas'][0]['value']
                roas_data=f'{float(roas_data):.2f}' 
                roas_data_list.append(roas_data)
            except:
                roas_data_list.append('None')
            #取得連結點擊次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='link_click':
                    link_clicks_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_clicks_list.append('None')
            save_index=0
            #取得購買次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='purchase':
                    pay_num_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                pay_num_list.append('None')
            save_index=0
            #計算 CVR 公式:購買次數÷連結點擊次數
            try:
                cvr_list.append(f'{int(pay_num_list[-1])/int(link_clicks_list[-1])*100:.2f}%')
            except:
                cvr_list.append('None')    
            #轉為小數點第二位與百分比
            #CTR(全部)，
            #改為FB-平均客單價，公式:購買轉換值÷購買次數
            try:
                ctr_cal=f'{float(buy_trans_data[-1])/float(pay_num_list[-1]):.2f}'
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
            #CPM    
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append(cpm_cal)
            except:
                cpm_list.append('None')
            #抽取加入購物車選項及存入容器
            cart_data = [trans['value'] for trans in actions_path if trans['action_type']=='add_to_cart']
            try:
                cart_list.append(cart_data[0])
            except:
                cart_list.append('None')
            #存入容器
            try:
                spend_list.append(insights[0]['spend'])
            except:
                spend_list.append('None')
            #曝光次數
            try:
                impressions_list.append(insights[0]['impressions'])
            except:
                impressions_list.append('None')
            #原本的點擊次數(全部)
            #改為CTR(連結點閱率)，計算公式:連結點擊次數/曝光次數*100%
            try:
                ctr_link_cal=f'{(float(link_clicks_list[-1])/float(impressions_list[-1])*100):.2f}%' 
                ctr_link_list.append(ctr_link_cal)
            except:
                ctr_link_list.append('None')
                
            #取得觸及人數
            #改為加入購物車率ACR，計算公式:加入購物車次數/連結頁面瀏覽次數*100%
            
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='landing_page_view':
                    link_page_view.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_page_view.append('None')
            save_index=0
            
            try:
                acr_cal=f'{float(cart_list[-1])/float(link_page_view[-1])*100:.2f}%'
                reach_list.append(acr_cal)
            except:
                reach_list.append('None')
            #存入每日日期
            date_list.append(cal_start_var)
            #
            if cal_start_var==cal_end_var: 
                break
            cal_start_var+=timedelta(days=1) 
            
        # print('******************************')
        # print(date_list)
        # print(reach_list)
        # print(spend_list)
        # print(impressions_list)
        # print(link_clicks_list)
        # print(clicks_list)
        # print(ctr_list)
        # print(cpm_list)
        # print(cart_list)
        # print(pay_num_list)
        # print(cvr_list)
        # print(roas_data_list)
        # print(result_cost_list)
        # print(buy_trans_list)
        
        #結果整理成dataframe
        ad_data = {
            meta_columns[0]:date_list,
            meta_columns[1]:spend_list,
            meta_columns[2]:impressions_list,
            meta_columns[3]:link_clicks_list,
            meta_columns[4]:ctr_link_list,
            meta_columns[5]:cart_list,
            meta_columns[6]:reach_list,
            meta_columns[7]:cpm_list,
            meta_columns[8]:result_cost_list,
            meta_columns[9]:pay_num_list,
            meta_columns[10]:cvr_list,
            meta_columns[11]:roas_data_list,
            meta_columns[12]:buy_trans_list,
            meta_columns[13]:ctr_list,
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
        
        for date_var in week_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',date_var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
            }
            # 查詢廣告層級的統計數據
            params = { 
                'time_range': time_range, 
                'fields': [ 
                    AdsInsights.Field.reach,#觸及人數
                    AdsInsights.Field.spend,  # 花費金額 
                    AdsInsights.Field.impressions,  # 曝光次數 
                    AdsInsights.Field.clicks,  # 總點擊次數 
                    AdsInsights.Field.ctr, # CTR(連結點閱率) 
                    AdsInsights.Field.cpm, # CPM(每千次廣告曝光成本) 
                    AdsInsights.Field.actions,#部分數據在活動
                    #AdsInsights.Field.conversions,
                    AdsInsights.Field.purchase_roas,
                    AdsInsights.Field.action_values,
                    AdsInsights.Field.cost_per_action_type,
                ], 
            }
            #獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params) 
            
            #購買轉換值:1580 purchase
            #[0]['cost_per_action_type'][0]['action_type]=='purchase'
            #"value": "2038"
            #purchase_roas[0]['value']:.2f
        
            #活動數據路徑
            actions_path=insights[0]['actions']
            #CPA路徑
            cost_actions_path=insights[0]['cost_per_action_type']
            #購買轉換值路徑
            buy_trans_path=insights[0]['action_values']
            
            # if len(insights) == 0: 
            #     cal_start_var+=timedelta(days=1) 
            #     if cal_start_var==cal_end_var: 
            #         break
            #     continue 

            #以下各項如果沒有數據就放入 None
            #儲存索引值，用於判斷以下容器 list 是否放入 None
            
            save_index=0
            #購買轉換值
            buy_trans_data = [trans['value'] for trans in buy_trans_path if trans['action_type'] == 'onsite_web_app_purchase']
            try:
                buy_trans_list.append(buy_trans_data[0])
            except:
                buy_trans_list.append('None')
            #每次成果成本
            result_cost_data = [trans['value'] for trans in cost_actions_path if trans['action_type'] == 'web_in_store_purchase']
            try:
                result_cost_list.append(result_cost_data[0])
            except:
                result_cost_list.append('None')
            
            #取得 roas 
            try:
                roas_data=insights[0]['purchase_roas'][0]['value']
                roas_data=f'{float(roas_data):.2f}' 
                roas_data_list.append(roas_data)
            except:
                roas_data_list.append('None')
            #取得連結點擊次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='link_click':
                    link_clicks_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_clicks_list.append('None')
            
            #取得購買次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='purchase':
                    pay_num_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                pay_num_list.append('None')
            #計算 CVR 公式:購買次數÷連結點擊次數
            try:
                cvr_list.append(f'{int(pay_num_list[-1])/int(link_clicks_list[-1])*100:.2f}%')
            except:
                cvr_list.append('None')    
            #轉為小數點第二位與百分比
            #CTR(全部)，
            #改為FB-平均客單價，公式:購買轉換值÷購買次數
            try:
                ctr_cal=f'{float(buy_trans_data[-1])/float(pay_num_list[-1]):.2f}'
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
            #CPM    
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append(cpm_cal)
            except:
                cpm_list.append('None')
            #抽取加入購物車選項及存入容器
            cart_data = [trans['value'] for trans in actions_path if trans['action_type']=='add_to_cart']
            try:
                cart_list.append(cart_data[0])
            except:
                cart_list.append('None')
            #存入容器
            try:
                spend_list.append(insights[0]['spend'])
            except:
                spend_list.append('None')
            
            try:
                impressions_list.append(insights[0]['impressions'])
            except:
                impressions_list.append('None')
            #原本的點擊次數(全部)
            #改為CTR(連結點閱率)，計算公式:連結點擊次數/曝光次數*100%
            try:
                ctr_link_cal=f'{(float(link_clicks_list[-1])/float(impressions_list[-1])*100):.2f}%' 
                ctr_link_list.append(ctr_link_cal)
            except:
                ctr_link_list.append('None')
                
            #取得觸及人數
            #改為加入購物車率ACR，計算公式:加入購物車次數/連結頁面瀏覽次數*100%
            
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='landing_page_view':
                    link_page_view.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_page_view.append('None')
            save_index=0
            
            try:
                acr_cal=f'{float(cart_list[-1])/float(link_page_view[-1])*100:.2f}%'
                reach_list.append(acr_cal)
            except:
                reach_list.append('None')
            
            date_list.append(date_var) 
        
        #結果整理成dataframe
        ad_data = {
            meta_columns[0]:date_list,
            meta_columns[1]:spend_list,
            meta_columns[2]:impressions_list,
            meta_columns[3]:link_clicks_list,
            meta_columns[4]:ctr_link_list,
            meta_columns[5]:cart_list,
            meta_columns[6]:reach_list,
            meta_columns[7]:cpm_list,
            meta_columns[8]:result_cost_list,
            meta_columns[9]:pay_num_list,
            meta_columns[10]:cvr_list,
            meta_columns[11]:roas_data_list,
            meta_columns[12]:buy_trans_list,
            meta_columns[13]:ctr_list,
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

        for date_var in month_date_list:
            date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',date_var)
            time_range = {
                'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
                'until': str(date_start_end[1])   # 替換為你想要的結束日期 
            }
            # 查詢廣告層級的統計數據
            params = { 
                'time_range': time_range, 
                'fields': [ 
                    AdsInsights.Field.reach,#觸及人數
                    AdsInsights.Field.spend,  # 花費金額 
                    AdsInsights.Field.impressions,  # 曝光次數 
                    AdsInsights.Field.clicks,  # 總點擊次數 
                    AdsInsights.Field.ctr, # CTR(連結點閱率) 
                    AdsInsights.Field.cpm, # CPM(每千次廣告曝光成本) 
                    AdsInsights.Field.actions,#部分數據在活動
                    #AdsInsights.Field.conversions,
                    AdsInsights.Field.purchase_roas,
                    AdsInsights.Field.action_values,
                    AdsInsights.Field.cost_per_action_type,
                ], 
            }
            #獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params) 
            
            #購買轉換值:1580 purchase
            #[0]['cost_per_action_type'][0]['action_type]=='purchase'
            #"value": "2038"
            #purchase_roas[0]['value']:.2f
        
            #活動數據路徑
            actions_path=insights[0]['actions']
            #CPA路徑
            cost_actions_path=insights[0]['cost_per_action_type']
            #購買轉換值路徑
            buy_trans_path=insights[0]['action_values']
            
            # if len(insights) == 0: 
            #     cal_start_var+=timedelta(days=1) 
            #     if cal_start_var==cal_end_var: 
            #         break
            #     continue 

            #以下各項如果沒有數據就放入 None
            #儲存索引值，用於判斷以下容器 list 是否放入 None
            
            save_index=0
            #購買轉換值
            buy_trans_data = [trans['value'] for trans in buy_trans_path if trans['action_type'] == 'onsite_web_app_purchase']
            try:
                buy_trans_list.append(buy_trans_data[0])
            except:
                buy_trans_list.append('None')
            #每次成果成本
            result_cost_data = [trans['value'] for trans in cost_actions_path if trans['action_type'] == 'web_in_store_purchase']
            try:
                result_cost_list.append(result_cost_data[0])
            except:
                result_cost_list.append('None')
            
            #取得 roas 
            try:
                roas_data=insights[0]['purchase_roas'][0]['value']
                roas_data=f'{float(roas_data):.2f}' 
                roas_data_list.append(roas_data)
            except:
                roas_data_list.append('None')
            #取得連結點擊次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='link_click':
                    link_clicks_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_clicks_list.append('None')
            
            #取得購買次數
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='purchase':
                    pay_num_list.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                pay_num_list.append('None')
            #計算 CVR 公式:購買次數÷連結點擊次數
            try:
                cvr_list.append(f'{int(pay_num_list[-1])/int(link_clicks_list[-1])*100:.2f}%')
            except:
                cvr_list.append('None')    
            #轉為小數點第二位與百分比
            #CTR(全部)，
            #改為FB-平均客單價，公式:購買轉換值÷購買次數
            try:
                ctr_cal=f'{float(buy_trans_data[-1])/float(pay_num_list[-1]):.2f}'
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
            #CPM    
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append(cpm_cal)
            except:
                cpm_list.append('None')
            #抽取加入購物車選項及存入容器
            cart_data = [trans['value'] for trans in actions_path if trans['action_type']=='add_to_cart']
            try:
                cart_list.append(cart_data[0])
            except:
                cart_list.append('None')
            #存入容器
            try:
                spend_list.append(insights[0]['spend'])
            except:
                spend_list.append('None')
            
            try:
                impressions_list.append(insights[0]['impressions'])
            except:
                impressions_list.append('None')
            
            #原本的點擊次數(全部)
            #改為CTR(連結點閱率)，計算公式:連結點擊次數/曝光次數*100%
            try:
                ctr_link_cal=f'{(float(link_clicks_list[-1])/float(impressions_list[-1])*100):.2f}%' 
                ctr_link_list.append(ctr_link_cal)
            except:
                ctr_link_list.append('None')
                
            #取得觸及人數
            #改為加入購物車率ACR，計算公式:加入購物車次數/連結頁面瀏覽次數*100%
            
            for var in range(len(actions_path)):
                if actions_path[var]['action_type']=='landing_page_view':
                    link_page_view.append(actions_path[var]['value'])
                    save_index=var
                    break
            if save_index==0:
                link_page_view.append('None')
            save_index=0
            
            try:
                acr_cal=f'{float(cart_list[-1])/float(link_page_view[-1])*100:.2f}%'
                reach_list.append(acr_cal)
            except:
                reach_list.append('None')
            
            date_list.append(date_var) 
        
        #結果整理成dataframe
        ad_data = {
            meta_columns[0]:date_list,
            meta_columns[1]:spend_list,
            meta_columns[2]:impressions_list,
            meta_columns[3]:link_clicks_list,
            meta_columns[4]:ctr_link_list,
            meta_columns[5]:cart_list,
            meta_columns[6]:reach_list,
            meta_columns[7]:cpm_list,
            meta_columns[8]:result_cost_list,
            meta_columns[9]:pay_num_list,
            meta_columns[10]:cvr_list,
            meta_columns[11]:roas_data_list,
            meta_columns[12]:buy_trans_list,
            meta_columns[13]:ctr_list,
        }
        ad_data_all=pd.DataFrame(ad_data)
        ad_data_all_view=st.dataframe(ad_data_all)

        single_date=st.selectbox('請選擇日期',date_list) 
        
        if single_date:
           date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
           view_ad_detile(date_filter[0], date_filter[1])
        
        # 打印每個月的日期範圍
        # for var in month_date_list:
        #     date_start_end=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',var)
        #     time_range = {
        #         'since': str(date_start_end[0]),  # 替換為你想要的開始日期 
        #         'until': str(date_start_end[1])   # 替換為你想要的結束日期 
        #     }
        #     # 查詢廣告層級的統計數據 
        #     params = { 
        #         'time_range': time_range, 
        #         'fields': [ 
        #             AdsInsights.Field.spend,  # 花費金額 
        #             AdsInsights.Field.impressions,  # 曝光次數 
        #             AdsInsights.Field.clicks,  # 總點擊次數 
        #             AdsInsights.Field.ctr, # CTR(連結點閱率) 
        #             AdsInsights.Field.cpm, # CPM(每千次廣告曝光成本) 
        #         ], 
        #     }
        #     # 獲取帳戶層級的統計數據 
        #     insights = my_account.get_insights(params=params)
            
        #     # 轉為小數點第二位與百分比 
        #     ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
        #     cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
        #     #存入容器
        #     spend_list.append(insights[0]['spend'])
        #     impressions_list.append(insights[0]['impressions'])
        #     clicks_list.append(insights[0]['clicks'])
        #     ctr_list.append(ctr_cal)
        #     cpm_list.append(cpm_cal)
        #     #存入每禮拜日期
        #     date_list.append(var) 
        
        #     #結果整理成dataframe
        # ad_data = {
        #     meta_columns[0]:date_list,
        #     meta_columns[1]:spend_list,
        #     meta_columns[2]:impressions_list,
        #     meta_columns[3]:clicks_list,
        #     meta_columns[4]:ctr_list,
        #     meta_columns[5]:cpm_list,
        #     meta_columns[6]:cart_list,
        # }
        # ad_data_all=pd.DataFrame(ad_data)
        # ad_data_all_view=st.dataframe(ad_data_all)
        # single_date=st.selectbox('請選擇日期',date_list)
        # if single_date:
        #     date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
        #     view_ad_detile(date_filter[0], date_filter[1])
    
    #uuspa_meta_api_link函式主程式
    my_app_id = '1777385229335734'
    my_app_secret = '2b35ce330a4c66dbde025764339aa179'
    my_access_token = 'EAAZAQhb85PLYBOZCbgBYmozJjkAfNOmArj26h51kMWasqTZCaKLEZCv64zflnlgj7r13wPt7xWFJSig2ESNI5tzzBrcsPKw7lsMArS0IiAYgiII1tYMRD4AeZCGbeDnmexqnHaQDqOYyi5KZAPqHgJqewH04g0cMsykSmrzSr4PGM4UoQAxbhByvqV5Rox3rCGZAuZCbALKh'
    # 初始化 Facebook 廣告 API 
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token) 
    # 指定你的廣告帳戶 ID 
    my_account = AdAccount('act_1316371069004495')
    #要顯示的欄位 
    #meta_columns=['日期','FB-加入購物車率','花費金額','FB-曝光次數','FB-點擊','FB-CTR(連結點閱率)','FB-平均客單價','FB-CPM(每千次廣告曝光成本)','FB-加入購物車','購買次數','FB-CVR','FB-ROAS','FB-CPA','FB-轉換價值'] 
    #調整次數
    meta_columns=['日期','花費金額','FB-曝光次數','FB-點擊','FB-CTR(連結點閱率)','FB-加入購物車','FB-加入購物車率','FB-CPM(每千次廣告曝光成本)','FB-CPA','FB-訂單數','FB-CVR轉換率','FB-ROAS','FB-轉換價值','FB-平均客單價',] 
    
    #儲存結果的容器
    date_list=[]
    spend_list=[]
    impressions_list=[]
    ctr_link_list=[]
    ctr_list=[]
    cpm_list=[]
    cart_list=[]
    pay_num_list=[]
    link_clicks_list=[]
    cvr_list=[]
    reach_list=[]
    roas_data_list=[]
    result_cost_list=[]
    buy_trans_list=[]
    #新增連結頁面瀏覽結果
    link_page_view=[]
    
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
        detile_ad_reach=[]
        detile_ad_cpc=[]
        # 指定開始和結束時間（Unix 時間戳） 
        params = { 
            'time_range': { 
            'since': str(start_search_date),  # 替換為你想要的開始日期 
            'until': str(end_search_date)   # 替換為你想要的結束日期 
            }, 
            'fields': ['name','id']
        }
        # 獲取廣告集 
        #ad_sets = my_account.get_ads(params=params) 
        
        
        my_app_id2 = '1549404199339644'
        my_app_secret2 = 'b2d77e99db3964fe68975d7a66107147'
        my_access_token2 = 'EAAWBLMbqRnwBOxZBURCbpAcZAJO3vknK1hO3F5O4JIsJU5M1ZCr9IdBqLVVZByPJ26yc6TYNn4WOfEKf18F3gYCplmmwjhZAzVlZBlZASfIqZBeFYZADMVx50WN5Aw2IDMPnLkYzWVuGUio0lQCZAhPfTQBD76P9Fvh9WvDFAxXF2zea5PEvDtKYsL7ukX4lIaCHdrIODGFo4O'
        # 初始化 Facebook 廣告 API 
        FacebookAdsApi.init(my_app_id2, my_app_secret2, my_access_token2) 
        # 指定你的廣告帳戶 ID 
        my_account2 = AdAccount('act_1033945910984802') 
        ad_sets = my_account2.get_ads(params=params)
        
        
        #要顯示的欄位 
        meta_columns=['廣告ID','廣告名稱','花費金額','曝光次數','觸及人數','點擊次數(全部)','CTR(全部)','CPM(每千次廣告曝光成本)','CPC(全部)'] 
        #迭代每個廣告集並獲取廣告 
        for ad in ad_sets: 
            #避免過量讀取 
            ti.sleep(0.5)
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
                    #新增測試
                    AdsInsights.Field.actions,
                    AdsInsights.Field.cpc,
                ],
                'time_range': { 
                    'since': str(start_search_date),  # 替換為你想要的開始日期 
                    'until': str(end_search_date)   # 替換為你想要的結束日期 
                } 
            } 
            
            insights = Ad(ad_id).get_insights(params=insights_params) 
            #print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
            
            for insight in insights:
                ti.sleep(0.5)
                try:
                    ctr_cal=f'{float(insight["ctr"]):.2f}%' 
                    detile_ad_ctr.append(ctr_cal)
                except:
                    detile_ad_ctr.append('None')
                    
                try:
                    cpm_cal=f'{float(insight["cpm"]):.2f}'
                    detile_ad_cpm.append('NT$'+str(round(float(cpm_cal))))
                except:
                    detile_ad_cpm.append('None')
                    
                #加入cpc
                try:
                    detile_ad_cpc.append('NT$'+str(round(float(insight['cpc']))))
                except:
                    detile_ad_cpc.append('None')
                #加入觸及人數
                try:
                    detile_ad_reach.append(insight['reach'])
                except:
                    detile_ad_reach.append('None')
                #各項廣告的細節依序存入容器
                detile_ad_num.append(ad_id)
                detile_ad_name.append(ad_name)
                
                try:
                    detile_ad_spend.append(insight['spend'])
                except:
                    detile_ad_spend.append('None')
                
                try:
                    detile_ad_impressions.append(insight['impressions'])
                except:
                    detile_ad_impressions.append('None')
                
                try:
                    detile_ad_clicks.append(insight['clicks'])
                except:
                    detile_ad_clicks.append('None')

        ad_data_detile = {
            meta_columns[0]:detile_ad_num,
            meta_columns[1]:detile_ad_name,
            meta_columns[2]:detile_ad_spend,
            meta_columns[3]:detile_ad_impressions,
            meta_columns[4]:detile_ad_reach,
            meta_columns[5]:detile_ad_clicks,
            meta_columns[6]:detile_ad_ctr,
            meta_columns[7]:detile_ad_cpm,
            meta_columns[8]:detile_ad_cpc,
        }
        ad_data_all_detile=pd.DataFrame(ad_data_detile)
        ad_data_all_detile_view=st.dataframe(ad_data_all_detile)
    
    #單日    
    def single_view_ad(start_date,end_date):
        
        cal_start_var=start_date
        cal_end_var=end_date
        while True:
            ti.sleep(0.5)
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
                    AdsInsights.Field.cpc,
                    AdsInsights.Field.reach,
                ], 
            }
            # 獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params) 
            
            if len(insights) == 0: 
                cal_start_var+=timedelta(days=1) 
                if cal_start_var==cal_end_var: 
                    break
                continue 
            #print(insights)
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            # 轉為小數點第二位與百分比
            try:
                ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
                
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append('NT$'+str(round(float(cpm_cal))))
            except:
                cpm_list.append('None')
                
            try:
                cpc_list.append('NT$'+str(round(float(insights[0]['cpc']))))
            except:
                cpc_list.append('None')
            
            try:
                reach_list.append(insights[0]['reach'])
            except:
                reach_list.append('None')
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
            meta_columns[4]:reach_list,
            meta_columns[5]:ctr_list,
            meta_columns[6]:cpm_list,
            meta_columns[7]:cpc_list,
        }
        ad_data_all=pd.DataFrame(ad_data)
        ad_data_all_view=st.dataframe(ad_data_all)
        
        date_list.insert(0, '請選擇日期')
        single_date=st.selectbox('請選擇日期',date_list)
        
        if single_date!='請選擇日期':
            view_ad_detile(single_date,single_date)
    
    #每禮拜
    def view_ad(start_date,end_date):
        
        dates=pd.date_range(start_date,end_date) 
        week_date_list=[]
        save_weeks=[] 
        current_weeks=[]
        
        for data_var in dates: 
            ti.sleep(0.5)
            if data_var.weekday()==0 and current_weeks: 
                save_weeks.append(current_weeks)
                current_weeks=[]
            current_weeks.append(data_var)
            
        if current_weeks:
            save_weeks.append(current_weeks)
            
        for key,value in enumerate(save_weeks):
            week_date_list.append(f'Week {key+1}: {value[0].date()}~{value[-1].date()}') 
        
        for var in week_date_list:
            ti.sleep(1)
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
                    AdsInsights.Field.cpc,
                    AdsInsights.Field.reach,
                ], 
            }
            # 獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params)
            # print(insights)
            # 轉為小數點第二位與百分比 
            try:
                ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
                
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append('NT$'+str(round(float(cpm_cal))))
            except:
                cpm_list.append('None')
                
            try:
                cpc_list.append('NT$'+str(round(float(insights[0]['cpc']))))
            except:
                cpc_list.append('None')
            
            try:
                reach_list.append(insights[0]['reach'])
            except:
                reach_list.append('None')
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            #存入每禮拜日期
            date_list.append(var)   
        
        #結果整理成dataframe
        
        ad_data = {
            meta_columns[0]:date_list,
            meta_columns[1]:spend_list,
            meta_columns[2]:impressions_list,
            meta_columns[3]:clicks_list,
            meta_columns[4]:reach_list,
            meta_columns[5]:ctr_list,
            meta_columns[6]:cpm_list,
            meta_columns[7]:cpc_list,
        }
        ad_data_all=pd.DataFrame(ad_data)
        ad_data_all_view=st.dataframe(ad_data_all)
        
        date_list.insert(0, '請選擇日期')
        single_date=st.selectbox('請選擇日期',date_list)
        
        if single_date!='請選擇日期':
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
            ti.sleep(0.5)
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
                    AdsInsights.Field.cpc,
                    AdsInsights.Field.reach,
                ], 
            }
            # 獲取帳戶層級的統計數據 
            insights = my_account.get_insights(params=params)
            # print(insights)
            # 轉為小數點第二位與百分比 
            try:
                ctr_cal=f'{float(insights[0]["ctr"]):.2f}%' 
                ctr_list.append(ctr_cal)
            except:
                ctr_list.append('None')
                
            try:
                cpm_cal=f'{float(insights[0]["cpm"]):.2f}' 
                cpm_list.append('NT$'+str(round(float(cpm_cal))))
            except:
                cpm_list.append('None')
                
            try:
                cpc_list.append('NT$'+str(round(float(insights[0]['cpc']))))
            except:
                cpc_list.append('None')
                
            try:
                reach_list.append(insights[0]['reach'])
            except:
                reach_list.append('None')
            #存入容器
            spend_list.append(insights[0]['spend'])
            impressions_list.append(insights[0]['impressions'])
            clicks_list.append(insights[0]['clicks'])
            #存入每禮拜日期
            date_list.append(var)   
        
        #結果整理成dataframe
        
        ad_data = {
            meta_columns[0]:date_list,
            meta_columns[1]:spend_list,
            meta_columns[2]:impressions_list,
            meta_columns[3]:clicks_list,
            meta_columns[4]:reach_list,
            meta_columns[5]:ctr_list,
            meta_columns[6]:cpm_list,
            meta_columns[7]:cpc_list,
        }
        ad_data_all=pd.DataFrame(ad_data)
        ad_data_all_view=st.dataframe(ad_data_all)
        
        date_list.insert(0, '請選擇日期')
        single_date=st.selectbox('請選擇日期',date_list)
        
        if single_date!='請選擇日期':
            date_filter=re.findall(r'\b\d{4}-\d{2}-\d{2}\b',single_date)
            view_ad_detile(date_filter[0], date_filter[1])
    
    #uupon_meta_api_link函式主程式
    my_app_id = '1234434214675152'
    my_app_secret = 'aae5dd5bbbf296a08f25582b503a3643'
    my_access_token = 'EAARithzdQtABOxA7ZA3zk6zE1qNmL540cqUoKrZCSKh17ZCRd8kUuACZCPlZBZAfsd3MZBZBB6DdhMAHFGzPZBrVaaymsYELgJrnLaUlINSQBgCyk4ZA3A1l9r5eF4aHTcZADcMdXI62WcgZCYfiMpF63PYZALK4h9Qd3V8nM7V9TzOLq4RHBSZADCnzGS5d1ZCZBiBtDZB4xcfpL3XOh'
    # 初始化 Facebook 廣告 API 
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token) 
    # 指定你的廣告帳戶 ID 
    my_account = AdAccount('act_1033945910984802') 
    
    #要顯示的欄位 
    meta_columns=['日期','花費金額','曝光次數','點擊次數(全部)','觸及人數','CTR(全部)','CPM(每千次廣告曝光成本)','CPC(全部)'] 
    #儲存結果的容器
    date_list=[]
    spend_list=[]
    impressions_list=[]
    clicks_list=[]
    ctr_list=[]
    cpm_list=[]
    cpc_list=[]
    reach_list=[]
    
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
    <p class="big-font">※溫馨小提示 : 為確保系統能正常執行，建議在操作上不要太過頻繁，看清楚選項再進行動作，查詢廣告數據的一次操作間隔五分鐘</p>
""", unsafe_allow_html=True)
st.write("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    <p class="big-font">⁂ 錯誤應對機制 : 先讓網頁休息5~10分鐘再進行作業</p>
""", unsafe_allow_html=True)
st.write("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    <p class="big-font">‼‼ 日期組合選擇單日時，日期範圍以不超過十五日為佳</p>
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
