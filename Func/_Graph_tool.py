import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
matplotlib.use('TkAgg')

def figure_plot(plug_time_list, plug_sp_raw_list, maf_result_list, \
    ref_time_list, ref_sp_list, df_bbi_raw, df_bbi_maf, df_bbi_ref, flag_ref,\
        User, Date, Trip_Num) :         
    x = 0
    y = 0
    for i in range(0, Trip_Num) : 
        
        try : 
            if len(df_bbi_ref[i]) != 0 : flag_ref = True
            else : flag_ref = False
        except : 
            flag_ref = False
            
        if flag_ref == False : 
            fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
            bbi_time_raw = df_bbi_raw[i].Time
            axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
            y_bbi_raw = np.zeros(len(bbi_time_raw))-5
            axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
            axes[0].legend()
            axes[0].grid()
            axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i+1))
            axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
            bbi_time_maf = df_bbi_maf[i].Time
            y_bbi_maf = np.zeros(len(bbi_time_maf))-5
            axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
            axes[1].legend()
            axes[1].grid()
            plt.get_current_fig_manager().window.wm_geometry(f"+{x}+{y}")
            if (i+1)%4== 0 : 
                y += 500
                x = 0
            else :
                x += 500
        elif flag_ref == True :
            fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
            bbi_time_raw = df_bbi_raw[i].Time
            axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
            y_bbi_raw = np.zeros(len(bbi_time_raw))-5
            axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
            axes[0].legend()
            axes[0].grid()
            axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i+1))
            axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
            bbi_time_maf = df_bbi_maf[i].Time
            y_bbi_maf = np.zeros(len(bbi_time_maf))-5
            axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
            axes[1].legend()
            axes[1].grid()

            bbi_time_and = df_bbi_ref[i].Time
            axes[2].plot(ref_time_list[i], ref_sp_list[i], 'b.', label='ref')
            y_bbi_and = np.zeros(len(bbi_time_and))-5
            axes[2].plot(bbi_time_and, y_bbi_and, '*')
            axes[2].legend()
            axes[2].grid()
            plt.get_current_fig_manager().window.wm_geometry(f"+{x}+{y}")
            if (i+1)%4== 0 : 
                y += 500
                x = 0
            else :
                x += 500
                
    plt.show(block=False)
    while True : 
        num = input("입력 : ")
        if num == 'c' : 
            plt.close('all')
            break
        time.sleep(1)
    
    
