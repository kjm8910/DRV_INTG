import matplotlib.pyplot as plt
import numpy as np
cnt_plot = 0
def figure_plot(plug_time_list, plug_sp_raw_list, maf_result_test, \
    ref_time_list, ref_sp_list, df_bbi_raw, df_bbi_maf, df_bbi_ref, flag_ref,\
        User, Date) :
    global cnt_plot 
    
        
    if flag_ref == False : 
        fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
        bbi_time_raw = df_bbi_raw.Time
        axes[0].plot(plug_time_list, plug_sp_raw_list, 'r.', label='plug')
        y_bbi_raw = np.zeros(len(bbi_time_raw))-5
        axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
        axes[0].legend()
        axes[0].grid()
        axes[0].set_title(User+' '+str(Date)+'!!!')
        axes[1].plot(plug_time_list, maf_result_test, 'g.', label='ma')
        bbi_time_maf = df_bbi_maf.Time
        y_bbi_maf = np.zeros(len(bbi_time_maf))-5
        axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
        axes[1].legend()
        axes[1].grid()

    elif flag_ref == True :
        fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
        bbi_time_raw = df_bbi_raw.Time
        axes[0].plot(plug_time_list, plug_sp_raw_list, 'r.', label='plug')
        y_bbi_raw = np.zeros(len(bbi_time_raw))-5
        axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
        axes[0].legend()
        axes[0].grid()
        axes[0].set_title(User+' '+str(Date)+'!!!')
        axes[1].plot(plug_time_list, maf_result_test, 'g.', label='ma')
        bbi_time_maf = df_bbi_maf.Time
        y_bbi_maf = np.zeros(len(bbi_time_maf))-5
        axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
        axes[1].legend()
        axes[1].grid()

        bbi_time_and = df_bbi_ref.Time
        axes[2].plot(ref_time_list, ref_sp_list, 'b.', label='ref')
        y_bbi_and = np.zeros(len(bbi_time_and))-5
        axes[2].plot(bbi_time_and, y_bbi_and, '*')
        axes[2].legend()
        axes[2].grid()

        
    #plt.show()
