from Func._Parsing import *
from Func._Filtering import *
from Func._BBI_Func import *
from Func._Analysis_tool import *
from Func._Graph_tool import * 

def Start_Simulation(SimMode, Date_List, User_List, Plug_List) : 
    start_date = int(Date_List[0])
    end_date = int(Date_List[1])
    
    if SimMode == 0 : 
        for User in User_List : 
            for cDate in range(start_date, end_date + 1) : 
                #### 1. 파싱 ######################################
                # a. Referece 유/무 판단 / 플러그 데이터 유/무 판단
                flag_and = Check_Android(cDate, User)
                flag_plug = Check_Plug(cDate, User)
                if flag_plug == False : break # 플러그 데이터 없으면 다음 데이터 확인
                # b. Parsing
                Plug_Data, Ref_Data = Parsing_Main(cDate, User, 0, flag_and)
                #### 2. 필터 & 예외처리 ##############################
                if flag_and == True : 
                    ref_ln_list = list(Ref_Data['latitude'])
                    ref_lt_list = list(Ref_Data['longitude'])
                    ref_sp_list = list(Ref_Data['speed']*3.6)
                    ref_ac_list = list(Ref_Data['accuracy'])
                    ref_time_list = list(Ref_Data['time'])
                
                plug_sp_list = list(Plug_Data['speed'])
                plug_sp_raw_list = list(Plug_Data['speed']) 
                plug_time_list = list(Plug_Data['ct'])
                plug_ln_list = list(Plug_Data['ln'])
                plug_lt_list = list(Plug_Data['lt'])
                plug_ac_list = list(Plug_Data['ac'])

                sp_maf_list = func_speed_filter(plug_time_list,\
                    plug_sp_list, plug_ac_list)
                #### 3. BBI Detection #############################
                df_raw_bbi, bbi_list_raw = \
                bbi_detection_no_exception(plug_time_list, plug_sp_raw_list,\
                    plug_ln_list, plug_lt_list)
                df_maf_bbi, bbi_list_maf = \
                bbi_detection_no_exception(plug_time_list, sp_maf_list,\
                    plug_ln_list, plug_lt_list)
                df_ref_bbi, bbi_list_ref = \
                bbi_detection_no_exception(ref_time_list, ref_sp_list,\
                    ref_ln_list, ref_lt_list)
                #### 4. 분석 결과 출력 ###############################
                # a. 지도, b. 그래프, c. BBI 결과
                if flag_and == False : bbi_list_ref = []
                print(str(cDate) +'//' + User)
                bbi_result_table(bbi_list_raw, bbi_list_maf, bbi_list_ref)
                
                ##########
                figure_plot(plug_time_list, plug_sp_raw_list, sp_maf_list,\
                    ref_time_list, ref_sp_list, df_raw_bbi, df_maf_bbi, \
                        df_ref_bbi, flag_and)
                
                ## LOWELL ##
                
                