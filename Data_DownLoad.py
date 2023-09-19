import datetime
from Func._AutoDataAdmin import *

# 1. Reference(Android) Data Download from FireBase
def Android_Data_Download() : 
    today = datetime.date.today()
    year = today.year
    PROJECT_PATH = Path('.').absolute()

    PROJECT_ID = "drv-bbi-test"

    cred = credentials.Certificate('/Users/jmkim/Documents/'+\
        'Finn_Python_Project/FireBase_KEY/'+\
            'drv-bbi-test-firebase-adminsdk-wpdve-3f64ab418b.json')
    try : 
        storage_admin = firebase_admin.get_app()
    except : 
        storage_admin = firebase_admin.initialize_app(cred,\
                        {'storageBucket':f"{PROJECT_ID}.appspot.com"})
        
    bucket = storage.bucket()

    blob = list(bucket.list_blobs())

    foler_path = r"/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/TEST_AND"
    
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

# 2. Plug Data Download from FireBase
def PLUG_Data_Download() : 
    today = datetime.date.today()
    year = today.year
    PROJECT_PATH = Path('.').absolute()

    PROJECT_ID = "drv-bbi-test"

    cred = credentials.Certificate('/Users/jmkim/Documents/'+\
        'Finn_Python_Project/FireBase_KEY/'+\
            'drv-bbi-test-firebase-adminsdk-wpdve-3f64ab418b.json')
    try : 
        storage_admin = firebase_admin.get_app()
    except : 
        storage_admin = firebase_admin.initialize_app(cred,\
                        {'storageBucket':f"{PROJECT_ID}.appspot.com"})
        
    bucket = storage.bucket()

    blob = list(bucket.list_blobs())

    foler_path = r"/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Plug/Test"
    
    for i in range(0, len(blob)) : 
        fb_file_name = blob[i].name
        if fb_file_name.find('txt') != -1 or fb_file_name.find('csv') != -1 : 
            ad = [i.start() for i in re.finditer('/', fb_file_name)]
            header = fb_file_name[:ad[0]]
            if len(ad) == 2 and header == 'PLUG_GNSS_DATA': 
                #ad_ymd = [i.start() for i in re.finditer('-', fb_file_name)]
                date_folder = fb_file_name[ad[0]+1:ad[1]]
                file_name = fb_file_name[ad[1]+1:]
                #if header == 'PLUG_GNSS_DATA' and date_folder[:4] == str(year): 
                os.makedirs(Path(foler_path,date_folder), exist_ok=True)
                blob_down = bucket.blob(fb_file_name)
                blob_down.download_to_filename(Path(foler_path,date_folder,file_name))
                if fb_file_name.find('.txt') != -1 : 
                    try : 
                        log = pd.read_csv(Path(foler_path,fb_file_name), delimiter=',') 
                        log.to_csv(foler_path+'/'+fb_file_name[:-10]+'.csv', index=None, mode='a')
                    except : 
                        print('error\n')

#Android_Data_Download()
PLUG_Data_Download()



