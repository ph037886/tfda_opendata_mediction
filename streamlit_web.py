import streamlit as st

def search_event(keyword):
    global final_result_container, option
    final_result_container.write(option)
    final_result_container.write(keyword)
    

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
    search_event(keyword)
if search_button:
    search_event(keyword)