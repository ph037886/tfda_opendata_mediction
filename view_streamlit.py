import sql_control
import pandas as pd
import translate_argos

def choose_button(column, keyword):
    df=sql_control.pd_read_sql(sql_control.search_medication_by_something(column,keyword))
    df=df.drop_duplicates(subset=['許可證字號'])
    return df

def final_result(license_code):
    df=sql_control.pd_read_sql(sql_control.search_for_streamlit(license_code))
    df=df[df['支付價']!='0.00']
    df['ATC_CODE中文翻譯']=df.apply(lambda row:translate_argos.translate_argos(row['ATC_CODE英文']), axix=1)
    df=df.iloc[0]
    return df
