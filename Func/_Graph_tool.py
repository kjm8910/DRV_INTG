import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def figure_plot(plug_time_list, plug_sp_raw_list, maf_result_list, \
    ref_time_list, ref_sp_list, df_bbi_raw, df_bbi_maf, df_bbi_ref, flag_ref,\
        User, Date, Trip_Num) :         
    if flag_ref == False : 
        for i in range(0, Trip_Num) : 
            fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
            bbi_time_raw = df_bbi_raw[i].Time
            axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
            y_bbi_raw = np.zeros(len(bbi_time_raw))-5
            axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
            axes[0].legend()
            axes[0].grid()
            axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i))
            axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
            bbi_time_maf = df_bbi_maf[i].Time
            y_bbi_maf = np.zeros(len(bbi_time_maf))-5
            axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
            axes[1].legend()
            axes[1].grid()
            
            
            
        plt.show()
    elif flag_ref == True :
        for i in range(0, Trip_Num) : 
            fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
            bbi_time_raw = df_bbi_raw.Time
            axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
            y_bbi_raw = np.zeros(len(bbi_time_raw))-5
            axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
            axes[0].legend()
            axes[0].grid()
            axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i))
            axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
            bbi_time_maf = df_bbi_maf.Time
            y_bbi_maf = np.zeros(len(bbi_time_maf))-5
            axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
            axes[1].legend()
            axes[1].grid()

            bbi_time_and = df_bbi_ref.Time
            axes[2].plot(ref_time_list[i], ref_sp_list[i], 'b.', label='ref')
            y_bbi_and = np.zeros(len(bbi_time_and))-5
            axes[2].plot(bbi_time_and, y_bbi_and, '*')
            axes[2].legend()
            axes[2].grid()
        plt.show()
    
    
    
def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)
