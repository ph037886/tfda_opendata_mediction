# tfda_opendata_mediction

下載台灣FDA的opendata，並製成Sqlite資料庫，細部資料的部分因為檔案很大gitgub不支援，無法上傳，程式執行就會自動產生最新的資料
### 主要用的的庫有7個
1. 藥品外觀'
2. ATC_code
3. 藥理治療分類
4. 仿單或外盒
5. 詳細處方成分
6. 全部藥品許可證
7. 健保藥品檔

### 程式主要流程：
1. download_new_source_and_update()：下載最新的資料，下載完會是zip檔，完成後解壓縮，刪除壓縮檔，留下json
2. json_to_sql()：解壓縮的json檔，在自動弄進Database裡面。這邊用語法讓SQL可以適應各種欄位數目，而不用一個一個調整
3. update_nhi_database()：健保藥品檔，健保藥品檔是csv，讀取方式也會不一樣，先讀成DataFrame。健保碼可以依邏輯去改為許可證字號，這樣就可以串接其他資料庫了
4. df_to_sql()：把剛剛健保檔的df轉成SQL

download_and_to_sql()：這個是一次執行所有步驟，第一次請直接執行這個

### 主要用途：
最主要當然是建檔，雖然還是少了一些資料，不過算是減少不少工作負擔。
藥物辨識可以串接paxlovid_drug_interaction (https://github.com/ph037886/paxlovid_drug_interaction )這支程式，步驟如下：
1. 用爬蟲或是複製的功能，去把雲端的資料弄出來
2. 健保碼和藥物辨識的Database去串接，就可以快速得到藥物外觀的敘述和連結
未來有時間再獨立寫一支出來

## 致謝：
這邊很感謝，臨床藥學會資訊委員會的賴建名 藥師，因為在2022/10/30聯合藥學研討會聽到賴藥師的分享才知道原來有這些資料庫，之前自己找都找不到。
