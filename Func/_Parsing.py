from pathlib import Path
import os
#import re
import pandas as pd

Path_Ref = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Android'
Path_Plug = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Plug/FB_Data'
Path_Data = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/'

def Parsing_Main(Date, User, Type, Flag_AND) : 
    # 1. Parsing PLUG
    Plug_Data = Parsing_Plug_Carrot(Date, User, Type)
    # 2. Parsing Android
    if Flag_AND == True : 
        Ref_Data = Parsing_AND_Carrot(Date, User)
    else : 
        Ref_Data = 0
    
    return Plug_Data, Ref_Data
        
    
    
def Parsing_AND_Carrot(Date, User) : 
    data_ref = []
    Date = str(Date)
    Date = Date[0:4]+'-'+Date[4:6]+'-'+Date[6:]
    PARSING_AND_PATH = Path(Path_Ref)
    AND_File_List = os.listdir(Path(PARSING_AND_PATH, Date))
    for ref_file in AND_File_List : 
        if ref_file.find(User.lower()) == 0 : 
            data_ref = pd.read_csv(Path(PARSING_AND_PATH, Date, ref_file))
            data_ref.sort_values(['time'])
            data_ref = data_ref.reset_index(drop = True)
            
    return data_ref
            
def Parsing_Plug_Carrot(Date, User, Type) : 
    data_plug = pd.DataFrame()
    Date = str(Date)
    PARSING_PLUG_PATH = Path(Path_Plug, Date)
    PLUG_File_List = os.listdir(PARSING_PLUG_PATH)
    
    for plug_file in PLUG_File_List : 
        if plug_file.find(User.lower()) != -1: 
            data_plug = pd.concat([data_plug, pd.read_csv(Path(PARSING_PLUG_PATH, plug_file))])# 파일
            data_plug.sort_values(['ct'])
            data_plug = data_plug.reset_index(drop = True)
    
    if len(data_plug) == 0 : 
        print(str(Date) + User + "No File!")
    
    return data_plug


    
           
def Check_Android(Date, User) : 
    PATH_AND = Path(Path_Data, 'Android')
    folder_list = os.listdir(PATH_AND)
    flag_and = False
    for folder_name in folder_list : 
        date_folder = folder_name.replace('-','')
        try : 
            file_list = os.listdir(Path(PATH_AND, folder_name))
            if date_folder == str(Date) : 
                for file_name in file_list : 
                    if file_name.find(User.lower()) == 0: 
                        flag_and = True
                        #파일 Path나 CSV 아웃풋으로 설정 
                        break
        except : 
            continue
    return flag_and

def Check_Plug(Date, User) : 
    PATH_AND = Path(Path_Data, 'Plug', 'FB_Data')
    folder_list = os.listdir(PATH_AND)
    flag_and = False
    for folder_name in folder_list : 
        date_folder = folder_name.replace('-','')
        if date_folder == str(Date) : 
            flag_and = True
            break
    return flag_and
            