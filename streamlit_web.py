import streamlit as st
import sql_control
import pandas as pd

def choose_box(keyword, option):
    df=sql_control.pd_read_sql(sql_control.search_medication_by_something(option, keyword))
    df=df.drop_duplicates(subset=['許可證字號'])

def search_event(keyword, option):
    global final_result_container, search_result_container
    search_result_container.wt('查詢結果：商品名 (學名)')

#final_result_container.dataframe(df)
    

#以下開始streamlit語法
st.set_page_config(page_title='藥品查詢-政府開放資源',layout="wide") #修改網頁title，並預設為寬廣模式

#以下開始功能區
option = st.selectbox('查詢欄位',('全部欄位','許可證字號','英文品名', '主成分',  '中文品名', '適應症', '外觀', 'ATCCODE', '健保碼'))
keyword=st.text_input('請輸入關鍵字')
search_button=st.button('搜尋',type="primary")
st.markdown("""---""")
final_result_container=st.container()
search_result_container=st.container()

st.write('網站內容資料來自政府開放平台')
st.write('Design by 國軍左營總醫院 臨床藥劑科 方志文 藥師')

if keyword:
    search_event(keyword, option)
if search_button:
    search_event(keyword, option)