import sqlite3
import pandas as pd

conn = sqlite3.connect('files/med_info.db')
cur=conn.cursor()

def do_sql(sql):
    """給Sqlite直接執行用，不經pandas"""
    cur.execute(sql)
    conn.commit()
    conn.close()
    
def pd_read_sql(sql):
    """給pandas讀取sql用"""
    df=pd.read_sql(sql,conn)
    return df

def del_no_use():
    sql="""
    DELETE 
    FROM 全部藥品許可證
    WHERE (註銷狀態='已廢止' OR 註銷狀態='已註銷')
    """
    return sql    

def create_view_for_stream():
    sql="""
    CREATE VIEW FOR_STREAMLIT AS 
    SELECT 全部藥品許可證.許可證字號
    , 全部藥品許可證.英文品名
    , 全部藥品許可證.主成分略述
    , 全部藥品許可證.中文品名
    , 全部藥品許可證.適應症
    , 全部藥品許可證.劑型
    , 全部藥品許可證.管制藥品分類級別
    , 藥品外觀.形狀
    , 藥品外觀.顏色
    , 藥品外觀.刻痕
    , 藥品外觀.外觀尺寸
    , 藥品外觀.標註一
    , 藥品外觀.標註二
    , 藥品外觀.外觀圖檔連結
    , 仿單或外盒.仿單圖檔連結
    , 仿單或外盒.外盒圖檔連結
    , ATC_code.主或次項
    , ATC_code.代碼 ATCCODE
    , ATC_code.英文分類名稱 ATC_CODE英文
    , 健保藥品清單.藥品代號 健保碼
    , 健保藥品清單.支付價
    , 健保藥品清單.給付規定章節
    , 健保藥品清單.給付規定章節連結
    , 健保藥品清單.藥品代碼超連結
    FROM 全部藥品許可證
    LEFT JOIN 藥品外觀 ON 全部藥品許可證.許可證字號=藥品外觀.許可證字號 
    LEFT JOIN 仿單或外盒 ON 全部藥品許可證.許可證字號=仿單或外盒.許可證字號 
    LEFT JOIN ATC_code ON 全部藥品許可證.許可證字號=ATC_code.許可證字號 
    LEFT JOIN 健保藥品清單 ON 全部藥品許可證.許可證字號=健保藥品清單.許可證字號 
    """
    return sql
    

def search_medication_by_something(column, keyword):
    """混合查詢欄位，查出許可證字號、英文品名、中文品名
    column：欄位名稱
    keyword：查詢關鍵字
    """
    keyword=keyword.upper()
    
    columns_dict={'許可證字號':'全部藥品許可證.許可證字號', 
                '英文品名':'全部藥品許可證.英文品名', 
                '主成分':'全部藥品許可證.主成分略述', 
                '中文品名':'全部藥品許可證.中文品名', 
                '適應症':'全部藥品許可證.適應症', 
                '形狀':'藥品外觀.形狀', 
                '顏色':'藥品外觀.顏色', 
                '刻痕':'藥品外觀.刻痕', 
                '外觀尺寸':'藥品外觀.外觀尺寸', 
                '標註一':'藥品外觀.標註一', 
                '標註二':'藥品外觀.標註二', 
                'ATCCODE':'ATC_code.代碼', 
                '健保碼':'健保藥品清單.藥品代號'}
    
    if column=='全部欄位':
        where_flied='WHERE ('
        for _, value in columns_dict.items():
            where_flied=where_flied + 'UPPER(' + value + ") like '%" + keyword + "%' OR "
        where_flied=where_flied[:-3]+')'
    elif column=='外觀':
        _list=['形狀',  '顏色', '刻痕', '外觀尺寸', '標註一', '標註二']
        where_flied='WHERE ('
        for i in _list:
            where_flied=where_flied + 'UPPER(' + columns_dict[i] + ") like '%" + keyword + "%' OR "
        where_flied=where_flied[:-3]+')'
    else:
        where_flied="WHERE " + 'UPPER(' + columns_dict[column] + ") like '%" + keyword + "%'"
    
    sql="""
    SELECT 全部藥品許可證.許可證字號
    , 全部藥品許可證.英文品名
    , 全部藥品許可證.主成分略述
    , 全部藥品許可證.中文品名
    FROM 全部藥品許可證
    LEFT JOIN 藥品外觀 ON 全部藥品許可證.許可證字號=藥品外觀.許可證字號 
    LEFT JOIN 仿單或外盒 ON 全部藥品許可證.許可證字號=仿單或外盒.許可證字號 
    LEFT JOIN ATC_code ON 全部藥品許可證.許可證字號=ATC_code.許可證字號 
    LEFT JOIN 健保藥品清單 ON 全部藥品許可證.許可證字號=健保藥品清單.許可證字號
    """
    
    sql=sql+where_flied
    return sql
    
def search_for_streamlit(license_code):
    sql="SELECT * FROM FOR_STREAMLIT WHERE 許可證字號 = '" + license_code +"'"
    return sql

if __name__=='__main__':
    print(search_medication_by_something('全部欄位','crestor'))
    pass