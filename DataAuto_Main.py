import datetime
from Func._AutoDataAdmin import *

flag_download_ref = [False, False]
Android_Data_Download()

while True : 
    # 1. Reference(Android) Data Download
    #   a. 매일 아침 4시, 6시 Reference(안드로이드) 데이터 로컬에 다운로드
    cTime = datetime.datetime.now()
    
    if cTime.hour >= 11 and flag_download_ref[0] == False : 
        Android_Data_Download()
        flag_download_ref[0] = True
    elif cTime.hour >= 12 and flag_download_ref[1] == False : 
        Android_Data_Download()
        flag_download_ref[1] = True
    elif cTime.hour >= 13 and flag_download_ref[1] == True :
         flag_download_ref[0] = False
         flag_download_ref[1] = False
    
    # 2. Plug Data upload to FB(Firebase)
    #   a. 플러그 데이터 메일로 전송(업무망), 수동(추후 자동화 예정)
    #   b. 메일 파싱(테크망), 오전 10시 이후 진행
    #   c. b 이후 첨부 파일(플러그 데이터) 로컬에 다운
    #   d. 압축 풀기
    #   e. FB에 플러그 데이터 업로드
    if cTime.hour >= 8 and cTime.hour <= 19 : 
        PlugData_Upload()
    else : 
        time.sleep(60*60)
    