#-*- coding: utf-8 -*-
import email
import imaplib
import os
import pandas as pd
import time
import re
import base64
import quopri
import zipfile
# Firebase 
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage
from pathlib import Path
import os
import datetime

# 1. Reference(Android) Data Download from FireBase
def Android_Data_Download() : 
    today = datetime.date.today()
    year = today.year
    PROJECT_PATH = Path('.').absolute()

    PROJECT_ID = "drv-bbi-test"

    cred = credentials.Certificate('//Users/jmkim/Documents/Finn_Python_Project/FireBase_KEY/'+\
            'drv-bbi-test-firebase-adminsdk-wpdve-3f64ab418b.json')
    try : 
        storage_admin = firebase_admin.get_app()
    except : 
        storage_admin = firebase_admin.initialize_app(cred,\
                        {'storageBucket':f"{PROJECT_ID}.appspot.com"})
        
    bucket = storage.bucket()

    blob = list(bucket.list_blobs())

    foler_path = r"/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Android"
    
    for i in range(0, len(blob)) : 
        fb_file_name = blob[i].name
        if fb_file_name.find('txt') != -1 or fb_file_name.find('csv') != -1 : 
            ad = [i.start() for i in re.finditer('/', fb_file_name)]
            
            if len(ad) == 3 : 
                header = fb_file_name[:ad[0]]
                ad_ymd = [i.start() for i in re.finditer('-', fb_file_name)]
                date_folder = fb_file_name[ad_ymd[0]+1:ad_ymd[2]+3]
                file_name = fb_file_name[ad[2]+1:]
            else : 
                ad_ymd = []
                date_folder = fb_file_name[:ad[0]]
            
            if len(date_folder) == 10 and date_folder[:4] == str(year): 
                os.makedirs(Path(foler_path,date_folder), exist_ok=True)
                blob_down = bucket.blob(fb_file_name)
                if len(ad_ymd) == 0 : 
                    blob_down.download_to_filename(Path(foler_path,fb_file_name))
                else : 
                    blob_down.download_to_filename(Path(foler_path,date_folder,file_name))
                if fb_file_name.find('.txt') != -1 : 
                    try : 
                        log = pd.read_csv(Path(foler_path,fb_file_name), delimiter=',') 
                        log.to_csv(foler_path+'/'+fb_file_name[:-10]+'.csv', index=None, mode='a')
                    except : 
                        print('error\n')
                        
# 2. Plug Data upload to FB(Firebase)
#   a. 플러그 데이터 메일로 전송(업무망), 수동(추후 자동화 예정)

#   c. b 이후 첨부 파일(플러그 데이터) 로컬에 다운
#   d. 압축 풀기
#   e. FB에 플러그 데이터 업로드
def PlugData_Upload() : 
    #   b. 메일 파싱(테크망), 오전 10시 이후 진행
    ROJECT_PATH = Path('.').absolute()

    PROJECT_ID = "drv-bbi-test" 
    cred = credentials.Certificate('//Users/jmkim/Documents/Finn_Python_Project/FireBase_KEY/'+\
            'drv-bbi-test-firebase-adminsdk-wpdve-3f64ab418b.json')
    
    try : 
        storage_admin = firebase_admin.get_app()
    except : 
        storage_admin = firebase_admin.initialize_app(cred,\
                        {'storageBucket':f"{PROJECT_ID}.appspot.com"})
        
    detach_dir = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Plug'
    # if 'attachments' not in os.listdir(detach_dir):
    #    os.mkdir('attachments')

    userName = 'jm89.kim@gmail.com' # 메일 계정
    passwd = 'krpzkazizhzhyiji' # 메일 비번
    while True : 
        try:
            imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
            typ, accountDetails = imapSession.login(userName, passwd)
            for i in imapSession.list()[1]:
                        l = i.decode().split(' "/" ')
                        print(l[0] + " = " + l[1])

            if typ != 'OK':
                print ('로그인 불가')
                raise

            imapSession.select('INBOX')                      # 사서함 이름
            typ, data = imapSession.search(None, '(FROM "gabriel@carrotins.com")')
            if typ != 'OK':
                print ('인박스 검색 중 에러 발생')
                raise
   
            # 모든 메일에 대해 반복 실행
            
            for msgId in data[0].split():
                typ, messageParts = imapSession.fetch(msgId, '(RFC822)')

                if typ != 'OK':
                    print ('메일 가져오는 중 에러 발생')
                    raise

                emailBody = messageParts[0][1]
                mail = email.message_from_bytes(emailBody)

                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    fileName = part.get_filename()
                    fileName = encoded_words_to_text(fileName)

                    #if bool(fileName):
                    filePath = os.path.join(detach_dir, 'Zip_Data',fileName)
                    #if not os.path.isfile(filePath) :
                    print(fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
            
           
            
            # 압출 풀기
            zip_file_list = os.listdir(detach_dir+'/Zip_Data')
            for file_name in zip_file_list : 
                if file_name.find('.zip') != -1 : 
                    date = file_name[:-4]
                    zipfile.ZipFile(f'{detach_dir}/Zip_Data/{file_name}').extractall(path=f'{detach_dir}/FB_Data/{date}/')   
                    bucket = storage.bucket()
                    dir_firebase = f'{detach_dir}/FB_Data/{date}/'
                    os.remove(detach_dir+'/Zip_Data/'+file_name)
            
            csv_folder_list = os.listdir(detach_dir+'/FB_Data')
            for folder in csv_folder_list : 
                dir_csv_folder = f'{detach_dir}/FB_Data/{folder}/'
                #full_name = os.path.join(dir_csv_folder)
                if os.path.isdir(dir_csv_folder):
                    file_csv_list = os.listdir(dir_csv_folder)
                else : 
                    continue
                for file_csv in file_csv_list : 
                    csv_path = dir_csv_folder +file_csv
                    date_ad = csv_path.rfind('/')
                    date = csv_path[date_ad-8:date_ad]
                    csvBlob = bucket.blob(f"PLUG_GNSS_DATA/{date}/{file_csv}")
                    csvBlob.upload_from_filename(csv_path)
            imapSession.close()
            imapSession.logout()
        except :
            # 압출 풀기
            zip_file_list = os.listdir(detach_dir+'/Zip_Data')
            for file_name in zip_file_list : 
                if file_name.find('.zip') != -1 : 
                    date = file_name[:-4]
                    zipfile.ZipFile(f'{detach_dir}/Zip_Data/{file_name}').extractall(path=f'{detach_dir}/FB_Data/{date}/')   
                    #os.remove(detach_dir+'/Zip_Data/'+file_name)
                    bucket = storage.bucket()
                    dir_firebase = f'{detach_dir}/FB_Data/{date}/'
            csv_folder_list = os.listdir(detach_dir+'/FB_Data')
            
            cTime = datetime.datetime.now()
            if cTime.hour >= 19 : 
                break
            else : 
                time.sleep(2)

def encoded_words_to_text(encoded_words):
    try:
        encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
        if encoding is 'B':
            byte_string = base64.b64decode(encoded_text)
        elif encoding is 'Q':
            byte_string = quopri.decodestring(encoded_text)
        return byte_string.decode(charset)
    except:
        return encoded_words