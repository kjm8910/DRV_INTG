#### Module Define ######################################
from Func._LUX1_Filtering import *
#### ####################################################

def func_speed_filter(plug_time_list, plug_sp_list, plug_ac_list, plug_type) : 
    if plug_type == 'LUX1' : 
        plug_sp_list = preprocessing_speed(plug_time_list, plug_sp_list)
        sp_maf_list = MovingAverageFilter(plug_time_list, plug_sp_list)    
        sp_result_list = BBI_Exception_Handle(plug_time_list, sp_maf_list)
    elif plug_type == 'AMT1' : 
        sp_result_list = 1
    elif plug_type == 'LUX2' : 
        sp_result_list = 1
    return sp_result_list