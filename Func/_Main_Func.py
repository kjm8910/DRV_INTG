from Func._Parsing import *
from Func._Filtering import *
from Func._BBI_Func import *
from Func._Analysis_tool import *
from Func._Graph_tool import * 

def Start_Simulation(SimMode, Date_List, User_List, Plug_List) : 
    start_date = int(Date_List[0])
    end_date = int(Date_List[1])
    trip_id = 0
    if SimMode == 0 : 
        for User in User_List : 
            for cDate in range(start_date, end_date + 1) : 
                #### 1. 파싱 ######################################
                # a. Referece 유/무 판단 / 플러그 데이터 유/무 판단
                flag_plug = Check_Plug(cDate, User)
                # b. Parsing
                if flag_plug == False : continue # 플러그 데이터 없으면 다음 데이터 확인
                else : 
                    flag_and = Check_Android(cDate, User)
                    Plug_Data, Ref_Data = Parsing_Main(cDate, User, 0, flag_and)
                    # c. 트립으로 나누기
                    Trip_Num, Plug_Data_Trip, Ref_Data_Trip = Data_Seperate_Trip(Plug_Data, flag_and, Ref_Data)
                    
                    #### 2. 필터 & 예외처리 ##############################
                    PLUG_RAW_SAVE = []
                    PLUG_TIME_SAVE = []
                    PLUG_MAF_SAVE = []
                    REF_RAW_SAVE = []
                    REF_TIME_SAVE = []                    
                    
                    DF_PLUG_SAVE = []
                    DF_PLUG_MAF_SAVE = []
                    DF_REF_SAVE = []
                    
                    for i in range(0, Trip_Num) : 
                        
                        if len(Ref_Data_Trip) == 0 :        flag_and = False
                        elif len(Ref_Data_Trip[i]) == 0:    flag_and = False
                        else :                              flag_and = True
                        
                        if flag_and == True : 
                            ref_ln_list = list(Ref_Data_Trip[i]['latitude'])
                            ref_lt_list = list(Ref_Data_Trip[i]['longitude'])
                            ref_sp_list = list(Ref_Data_Trip[i]['speed']*3.6)
                            ref_ac_list = list(Ref_Data_Trip[i]['accuracy'])
                            ref_time_list = list(Ref_Data_Trip[i]['time'])
                            
                            # DATA SAVE
                            REF_TIME_SAVE.append(ref_time_list)
                            REF_RAW_SAVE.append(ref_sp_list)
                        else : 
                            REF_TIME_SAVE.append([])
                            REF_RAW_SAVE.append([])
                                                
                        try : 
                            plug_sp_list = list(Plug_Data_Trip[i]['speed'])
                            plug_sp_raw_list = list(Plug_Data_Trip[i]['speed']) 
                        except : 
                            plug_sp_list = list(Plug_Data_Trip[i]['sp'])
                            plug_sp_raw_list = list(Plug_Data_Trip[i]['sp']) 
                        plug_time_list = list(Plug_Data_Trip[i]['ct'])
                        plug_ln_list = list(Plug_Data_Trip[i]['ln'])
                        plug_lt_list = list(Plug_Data_Trip[i]['lt'])
                        plug_ac_list = list(Plug_Data_Trip[i]['ac'])

                        sp_maf_list = func_speed_filter(plug_time_list,\
                            plug_sp_list, plug_ac_list)

                        ### DATA SAVE ####
                        PLUG_TIME_SAVE.append(plug_time_list)
                        PLUG_RAW_SAVE.append(plug_sp_raw_list)
                        PLUG_MAF_SAVE.append(sp_maf_list)
                        
                        #### 3. BBI Detection #############################
                        # 1 : 급출발, 2: 급가속, 3 : 급정지, 4 : 급감속
                        df_raw_bbi, bbi_list_raw = \
                        bbi_detection_no_exception(plug_time_list, plug_sp_raw_list,\
                            plug_ln_list, plug_lt_list)
                        df_maf_bbi, bbi_list_maf = \
                        bbi_detection_no_exception(plug_time_list, sp_maf_list,\
                            plug_ln_list, plug_lt_list)
                        DF_PLUG_SAVE.append(df_raw_bbi)
                        DF_PLUG_MAF_SAVE.append(df_maf_bbi)
                        if flag_and == True :
                            df_ref_bbi, bbi_list_ref = \
                            bbi_detection_no_exception(ref_time_list, ref_sp_list,\
                                ref_ln_list, ref_lt_list)
                            DF_REF_SAVE.append(df_ref_bbi)
                        else : 
                            df_ref_bbi = []
                            ref_time_list = []
                            ref_sp_list = []
                            
                        #### 4. 분석 결과 출력 ###############################
                        # a. 지도, b. 그래프, c. BBI 결과
                        if flag_and == False : bbi_list_ref = []
                        print(str(cDate) +' ' + User+' '+'Trip No.' + str(i+1))
                        bbi_result_table(bbi_list_raw, bbi_list_maf, bbi_list_ref, i)
                        print('\n')
                        
                    ########## Plot Graph ################
                    figure_plot(PLUG_TIME_SAVE, PLUG_RAW_SAVE, PLUG_MAF_SAVE,\
                        REF_TIME_SAVE, REF_RAW_SAVE, DF_PLUG_SAVE, DF_PLUG_MAF_SAVE, \
                            DF_REF_SAVE, User, cDate, Trip_Num)
                    
                        ########## 
                        #folium_map(plug_lt_list, plug_ln_list, df_maf_bbi, cDate, User, 'MAF')
                        ## LOWELL ##
