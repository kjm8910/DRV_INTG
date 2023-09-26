from pathlib import Path
import os
#import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
Path_Plug = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Plug/FB_Data'
Path_Ref = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV/Android'
Path_Data = '/Users/jmkim/Documents/Finn_Python_Project/Data/DRV'
#Path_Plug = '/Volumes/Data Lab/0. DRV/2. DRV_DATA/Plug/FB_Data'
#Path_Ref = '/Volumes/Data Lab/0. DRV/2. DRV_DATA/Android'
#Path_Data = '/Volumes/Data Lab/0. DRV/2. DRV_DATA'

def Parsing_Main(Date, User, Type, Flag_AND) : 
    # 1. Parsing PLUG
    Plug_Data = Parsing_Plug_Carrot(Date, User, Type)
    # 2. Parsing Android
    if Flag_AND == True : 
        Ref_Data = Parsing_AND_Carrot(Date, User)
    else : 
        Ref_Data = []
    
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
        if plug_file.find(User) != -1: 
            data_plug = pd.concat([data_plug, pd.read_csv(Path(PARSING_PLUG_PATH, plug_file))])# 파일 
            # ln lt == 0 && ac = 0 & 100
            idx = data_plug[data_plug['ln'] == 0].index
            data_plug.drop(idx , inplace=True)
            idx = data_plug[data_plug['ac'] == 0].index
            data_plug.drop(idx , inplace=True)
            idx = data_plug[data_plug['ac'] == 100].index
            data_plug.drop(idx , inplace=True) 
            
            #idx = data_plug[data_plug['ct'] <= 1692000000000].index
            #data_plug.drop(idx , inplace=True)
            #idx = data_plug[data_plug['ct'] >= 2000000000000].index
            #data_plug.drop(idx , inplace=True)
            
            data_plug.sort_values(['trip_id','ct'])
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
                    file_name = file_name.lower()
                    if file_name.find(User.lower()) != -1: 
                        flag_and = True
                        #파일 Path나 CSV 아웃풋으로 설정 
                        break
        except : 
            continue
    return flag_and

def Check_Plug(Date, User) : 
    PATH_PLUG = Path(Path_Plug)
    folder_list = os.listdir(PATH_PLUG)
    flag_plug = False
    for folder_name in folder_list : 
        date_folder = folder_name.replace('-','')
        try : 
            if date_folder == str(Date) : 
                file_list = os.listdir(Path(PATH_PLUG, folder_name))
                for file_name in file_list : 
                    file_name = file_name.lower()
                    if file_name.find(User.lower()) != -1: 
                        flag_plug = True
                        break
        except : 
            continue
        
    return flag_plug

def Data_Seperate_Trip(Plug_Data, flag_and, Ref_Data) : 
    
    Plug_Data_Trip_list = []
    Ref_Data_Trip_list = []
    trip_number = max(Plug_Data.trip_id)
    ad_ref = 0
    #0. 트립 아이디로 데이터 분리
    for i in range(0, trip_number) : 
        cTrip_id = i + 1
        Plug_Data_Trip_list.append(Plug_Data[Plug_Data.trip_id == cTrip_id])
        if flag_and == True : 
        
            try : 
                mask = (Ref_Data.time[ad_ref:] <= max(Plug_Data_Trip_list[i].ct)) & (Ref_Data.time[ad_ref:] >= min(Plug_Data_Trip_list[i].ct))
                Ref_Data_Trip_list.append(Ref_Data[ad_ref:].loc[mask])
                ad_ref += (len(Ref_Data_Trip_list[i-1]) + 1)
            except : 
                Ref_Data_Trip_list.append(pd.DataFrame([]))
        else : 
            Ref_Data_Trip_list.append([])
        
    return trip_number, Plug_Data_Trip_list, Ref_Data_Trip_list