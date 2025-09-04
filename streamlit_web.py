import streamlit as st
import view_streamlit as vs
import pandas as pd

def choose_box(args):
    global final_result_container
    final_result_container.empty()
    final_result_container.write(args)
    df=vs.final_result(args)
    final_result_container.dataframe(df)


def search_event(keyword, option):
    global search_result_container,final_result_container
    if keyword=='':
        pass
    else:
        search_result_container.empty() #清空本來的container
        final_result_container.empty()
        df=vs.choose_button(option, keyword)
        i=0
        while i < len(df):
            locals()['number'+str(i)] =search_result_container.button(df.iloc[i,1] + '(' +df.iloc[i,2]+')',key=i,help=df.iloc[i,3],on_click=choose_box,args=(df.iloc[i,0],))
            i+=1
        search_result_container.markdown("""---""")

#final_result_container.dataframe(df)
    

#以下開始streamlit語法
st.set_page_config(page_title='藥品查詢-政府開放資源',layout="wide") #修改網頁title，並預設為寬廣模式
st.markdown('## 藥品查詢-政府開放資源') #用markdown可以讓title變得比較小，比較好看
#以下開始功能區
option = st.selectbox('查詢欄位',('全部欄位','許可證字號','英文品名', '主成分',  '中文品名', '適應症', '外觀', 'ATCCODE', '健保碼'))
keyword=st.text_input('請輸入關鍵字')
search_button=st.button('搜尋',type="primary")
st.markdown("""---""")
search_result_container=st.container()
final_result_container=st.container()


st.write('網站內容資料來自政府開放平台')
st.write('Design by 國軍左營總醫院 臨床藥劑科 方志文 藥師')

if keyword:
    search_event(keyword, option)
if search_button:
    search_event(keyword, option)