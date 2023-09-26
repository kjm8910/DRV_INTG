from Func._Parsing import *
from Func._Filter import *
from Func._LUX1_Filtering import *
from Func._BBI_Func import *
from Func._Analysis_tool import *
from Func._Graph_tool import * 
from Func._map_tool import *

def Start_Simulation(SimMode, Date_List, User_List, Plug_List) : 
    start_date = int(Date_List[0])
    end_date = int(Date_List[1])
    trip_id = 0
    if SimMode == 0 : 
        for User in User_List : 
            for cDate in range(start_date, end_date + 1) :
                #### 1. 파싱 ######################################
                # a. Referece 유/무 팝단 / 플러그 띰이터 유/무 팝단
                flag_plug = Check_Plug(cDate, User)
                # b. Parsing
                if flag_plug == False : continue # 플러그 띰이터 없으면 다음 띰이터 확인
                else : 
                    flag_and = Check_Android(cDate, User)
                    Plug_Data, Ref_Data = Parsing_Main(cDate, User, 0, flag_and)
                    Plug_Type = Plug_Data.dvc_id[0]
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
                            plug_sp_list, plug_ac_list, Plug_Type)

                        ### DATA SAVE ####
                        PLUG_TIME_SAVE.append(plug_time_list)
                        PLUG_RAW_SAVE.append(plug_sp_raw_list)
                        PLUG_MAF_SAVE.append(sp_maf_list)
                        
                        #### 3. BBI Detection #############################
                        # 1 : 급출발, 2: 급가솝, 3 : 급정지, 4 : 급객솝
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
                            DF_REF_SAVE.append(df_ref_bbi)
                            
                        #### 4. 분석 결과 출력 ###############################
                        # a. 지띄, b. 그래프, c. BBI 결과
                        if flag_and == False : bbi_list_ref = []
                        print("==========================================")
                        print(str(cDate) +' ' + User+' '+'Trip No.' + str(i+1))
                        Trip_time_sec = (max(plug_time_list) - min(plug_time_list))/1000
                        Trip_time = time.strftime('%H:%M:%S', time.gmtime(Trip_time_sec))
                        print("Trip Total Time : "+str(Trip_time))
                        num_dt_over = count_dt_over(plug_time_list)
                        print("DT >= 2 : ", str(num_dt_over))
                        bbi_result_table(bbi_list_raw, bbi_list_maf, bbi_list_ref, i)
                        print("==========================================")
                        print('\n')
                        
                        ## LOWELL ##
                        '''
                        plot_main(
                            t_plug=plug_time_list, t_ref=ref_time_list, sp_plug=plug_sp_raw_list,
                            sp_plug_filter=sp_maf_list, sp_ref=ref_sp_list, df_bbi_plug=df_raw_bbi,
                            df_bbi_plug_filter=df_maf_bbi, df_bbi_ref=df_ref_bbi,
                            user_str=User, trip_str=str(i), date_str=str(cDate), dvc_str=Plug_List[0]
                        )
                        '''
                        
                        ## Hannah
                        '''
                        m = draw_map(plug_lt_list,plug_ln_list, plug_time_list,\
                            plug_sp_raw_list, sp_maf_list, df_raw_bbi, df_maf_bbi)
                        save_path = str(cDate)+'_'+str(User)+'.html'
                        m.save(save_path)
                        if flag_and == True:
                            m_ref = draw_map_rtk(plug_lt_list,plug_ln_list, plug_time_list, \
                                plug_sp_raw_list, sp_maf_list, df_raw_bbi, df_maf_bbi, \
                                ref_lt_list, ref_ln_list, ref_time_list, ref_sp_list, \
                                    df_ref_bbi)
                            save_path = str(cDate)+'_'+str(User)+'_ref.html'
                            m_ref.save(save_path) 
                            '''
                    ########## Plot Graph ################
                    figure_plot(PLUG_TIME_SAVE, PLUG_RAW_SAVE, PLUG_MAF_SAVE,\
                        REF_TIME_SAVE, REF_RAW_SAVE, DF_PLUG_SAVE, DF_PLUG_MAF_SAVE, \
                            DF_REF_SAVE, User, cDate, Trip_Num)
