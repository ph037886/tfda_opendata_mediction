#pip install pandas openpyxl xlrd requests

import requests
import sqlite3
import json
import zipfile
import os
import pandas as pd

def json_to_sql(path):
    conn=sqlite3.connect('files/med_info.db') #連線SQLite，沒有檔案的話會自己創一個新的
    json_file=json.load(open(path,encoding='utf-8')) #打開json
    table_name=os.path.splitext(path)[0].split('/')[-1] #用檔名當table的名稱
    
    #取得欄位名稱
    columns=[]
    column=[]
    for data in json_file:
        column=list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)

    value=[]
    values=[]
    for data in json_file:
        for i in columns:
            value.append(str(dict(data).get(i)))
        values.append(list(value))
        value.clear()

    columns_name=str()
    question_mark=str()
    for i in columns:
        columns_name=columns_name+','+i
        question_mark=question_mark+',?'
    columns_name=columns_name[1:]
    question_mark=question_mark[1:]
    
    create_query = 'create table if not exists '+table_name+' ('+columns_name+')'
    insert_query = 'insert into '+table_name+' values ('+question_mark+')'
    c = conn.cursor()
    c.execute(create_query)
    c.executemany(insert_query, values)
    conn.commit()
    c.close()

def download_new_source_and_update():
    #食藥署 open data https://data.fda.gov.tw/
    from_tfda={'藥品外觀':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=42&logType=5',
               'ATC_code':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=41&logType=5',
               '藥理治療分類AHFS':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=40&logType=5',
               '仿單或外盒':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=39&logType=5',
               '詳細處方成分':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=43&logType=5',
               '全部藥品許可證':'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=36&logType=5'}
    for name, url in from_tfda.items():
        response = requests.get(url)
        open('files/from_tfda/temp.zip', "wb").write(response.content)
        temp_zip=zipfile.ZipFile('files/from_tfda/temp.zip', 'r')
        #print(temp_zip.namelist()[0])
        temp_zip.extractall(path='files/from_tfda')
        try:
            os.rename('files/from_tfda/'+temp_zip.namelist()[0],'files/from_tfda/'+name+'.json')
        except FileExistsError:
            os.remove('files/from_tfda/'+name+'.json')
            json_to_sql('files/from_tfda/'+name+'.json')
            os.rename('files/from_tfda/'+temp_zip.namelist()[0],'files/from_tfda/'+name+'.json')
    temp_zip.close()
    os.remove('files/from_tfda/temp.zip')

def nhi_to_license(nhi_database): #舊方法，用健保碼轉衛署字號，可能會有部分轉錯的問題
    license_convert={'A':'衛署藥製',
                    'B':'衛署藥輸',
                    'J':'衛署菌疫製',
                    'K':'衛署菌疫輸',
                    'N':'內衛藥製',
                    'P':'內衛藥輸',
                    'R':'內衛菌疫製',
                    'S':'內衛菌疫輸',
                    'V':'衛署罕藥輸',
                    'W':'衛署罕藥製',
                    'Y':'衛署罕菌疫輸',
                    'Z':'衛署罕菌疫製'}
    nhi_database['許可證字號']=''
    i=0
    while i<len(nhi_database):
        try:
            nhi_database.iloc[i,10]=license_convert.get(nhi_database.iloc[i,4][0:1])+'字第0'+str(nhi_database.iloc[i,4][2:7])+'號'
            i+=1
        except TypeError:
            nhi_database.iloc[i,10]='專案藥品'
            i+=1

def update_nhi_database():
    def link_to_license(row):
        try:
            license_convert_link={'01':'衛署藥製',
                                '02':'衛署藥輸',
                                '03':'衛署成製',
                                '04':'衛署中藥輸',
                                '09':'衛署菌疫製',
                                '10':'衛署菌疫輸',
                                '12':'內衛藥製',
                                '13':'內衛藥輸',
                                '14':'內衛成製',
                                '15':'內衛菌疫製',
                                '16':'內衛菌疫輸',
                                '18':'署藥兼食製',
                                '19':'衛署成輸',
                                '20':'衛署罕藥輸',
                                '21':'衛署罕藥製',
                                '22':'衛署罕菌疫輸',
                                '23':'衛署罕菌疫製',
                                '41':'衛署藥陸輸',
                                '51':'衛部藥製',
                                '52':'衛部藥輸',
                                '53':'衛部成製',
                                '59':'衛部菌疫製',
                                '60':'衛部菌疫輸',
                                '68':'部藥兼食製',
                                '69':'衛部成輸',
                                '70':'衛部罕藥輸',
                                '71':'衛部罕藥製',
                                '72':'衛部罕菌疫輸',
                                '73':'衛部罕菌疫製',
                                '91':'衛部藥陸輸',
                                '99':'衛署菌製'}
            if row['藥品代號'][0:1]=='X':
                row['許可證字號']='專案藥品，無許可證字號'    
            else:
                row['許可證字號']=license_convert_link[row['藥品代碼超連結'][-8:-6]]+'字第'+row['藥品代碼超連結'][-6:]+'號'
        except:
            row['許可證字號']='許可證字號轉換錯誤'
        return row
    #url='https://data.nhi.gov.tw/Datasets/DatasetResource.ashx?rId=A21030000I-E41001-001'
    url='https://info.nhi.gov.tw/api/iode0000s01/Dataset?rId=A21030000I-E41001-001'
    response = requests.get(url)
    open('files/from_tfda/健保用藥品項查詢項目檔_健保用藥品項.csv', "wb").write(response.content)
    nhi_database=pd.read_csv(r'files/from_tfda/健保用藥品項查詢項目檔_健保用藥品項.csv',low_memory=False)
    nhi_database=nhi_database.sort_values('有效迄日',ascending=False)
    nhi_database=nhi_database.drop_duplicates(subset=['藥品代號'],keep='first')
    #nhi_database=nhi_database[['藥品英文名稱', '藥品中文名稱', '成份', 'ATC_CODE', '藥品代號', '單複方', '劑型', '製造廠名稱', '規格量', '規格單位']]
    nhi_database=nhi_database.fillna('')
    #nhi_database.to_pickle(r'files\nhi_med.pkl')
    nhi_database=nhi_database.apply(link_to_license,axis=1)
    df_to_sql(nhi_database)
    #return nhi_database

def df_to_sql(df):
    conn = sqlite3.connect('files/med_info.db')
    table_name='健保藥品清單'
    columns_name=str()
    for i in df.columns.to_list():
        columns_name=columns_name+','+i
    columns_name=columns_name[1:]
    create_query = 'create table if not exists '+table_name+' ('+columns_name+')'
    c = conn.cursor()
    c.execute(create_query)
    conn.commit()
    df.to_sql(table_name, conn, if_exists='replace', index=False) 
    c.close()
    
def download_and_to_sql():
    download_new_source_and_update()
    # 指定要列出所有檔案的目錄
    folder_path = "files/from_tfda/"
    # 遞迴列出所有檔案的絕對路徑
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            fullpath = os.path.join(root, f)
            if os.path.splitext(fullpath)[1]=='.json':
                json_to_sql(fullpath)
    update_nhi_database()

if __name__=='__main__':
    download_and_to_sql()