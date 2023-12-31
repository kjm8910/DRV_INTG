from functools import partial
from typing import Tuple
from pathlib import Path
import webbrowser
import numpy as np
import plotly.subplots as plotly_subplots
import plotly.graph_objects as plotly_go
import matplotlib.pyplot as plt
import matplotlib
import time
import seaborn as sns
matplotlib.use('TkAgg')

def figure_plot(plug_time_list, plug_sp_raw_list, maf_result_list, \
    ref_time_list, ref_sp_list, df_bbi_raw, df_bbi_maf, df_bbi_ref, \
        User, Date, Trip_Num) :         
    x = 0
    y = 0
    for i in range(0, Trip_Num) : 
        
        try : 
            if len(ref_sp_list[i]) != 0 : flag_ref = True
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
        
def plot_main(
    t_plug, t_ref, sp_plug, sp_plug_filter, sp_ref,
    df_bbi_plug, df_bbi_plug_filter, df_bbi_ref,
    user_str=None, trip_str=None, date_str=None, dvc_str=None
):

    #save_path = Path(Path('.').absolute(), 'results', 'figures', user_str, date_str)
    save_path = Path('/Users/jmkim/Documents/Finn_Python_Project/DRV_INTG_RESULT',user_str, date_str)
    save_path.mkdir(exist_ok=True, parents=True)
    file_name_1 = f'{dvc_str}_{trip_str}_comparison_result.html'
    file_name_2 = f'{dvc_str}_{trip_str}_comparison_result.png'

    nms = ['raw', 'filter']
    times = [t_plug, t_plug]
    speeds = [sp_plug, sp_plug_filter]
    bbi_idxs = [
        np.where(np.isin(np.array(t_plug), np.array(df_bbi_plug.Time))),
        np.where(np.isin(np.array(t_plug), np.array(df_bbi_plug_filter.Time))),
    ]
    if len(t_ref) > 0:
        nms = nms + ['reference']
        times = times + [t_ref]
        speeds = speeds + [sp_ref]
        bbi_idxs = bbi_idxs + [
            np.where(np.isin(np.array(t_ref), np.array(df_bbi_ref.Time)))
        ]

    plotly_comparison_results(
        nms=nms, times=times, speeds=speeds, behavior_results=None, behavior_idxs=bbi_idxs,
        alpha=.7, suptitle='<b>Comparison results for each filtering method</b>',
        save_file_name=Path(save_path, file_name_1), show=False, browser=False, return_fig=False
    )
    mpl_comparison_results(
        nms=nms, times=times, speeds=speeds, behavior_results=None, behavior_idxs=bbi_idxs,
        alpha=.7, suptitle='<b>Comparison results for each filtering method</b>',
        save_file_name=Path(save_path, file_name_2), show=False, return_fig=False
    )


def plotly_comparison_results(
        nms: Tuple[str, ...], times: Tuple[np.ndarray, ...], speeds: Tuple[np.ndarray, ...],
        behavior_results: Tuple[np.ndarray, ...] = None, behavior_idxs: Tuple[np.ndarray, ...] = None,
        suptitle: str = None,
        relative_time: bool = True, alpha: float = 7, save_file_name: Path = None, show: bool = False,
        browser: bool = False, return_fig: bool = False
):

    """
    Plot the comparison results for testing the BBI using plotly

    :param nms: Tuple of names of method to generate subplots
    :param times: Tuple of time for each result
    :param speeds: Tuple of speed for each result
    :param behavior_results: Tuple of behavior result for each result. 4xn shape array, of which columns mean accel,
    deaccel, start, stop, respectively
    :param suptitle: add supertitle in figure with str value
    :param relative_time: normalize the time with start = 0
    :param alpha: the float value for opacity of object in figure
    :param show:
    :param browser:
    :param return_fig:
    :param save_file_name: file path to save with html format
    :return: plotly object
    """

    if not isinstance(times[0], np.ndarray):
        times = tuple(map(np.array, times))
    if not isinstance(speeds[0], np.ndarray):
        speeds = tuple(map(np.array, speeds))
    if behavior_results is not None:
        if not isinstance(behavior_results[0], np.ndarray):
            behavior_results = tuple(map(np.array, behavior_results))

    if relative_time:
        times = list(map(lambda t: (t - t[0]) / 1000, times))

    if behavior_idxs is not None:
        behavior_times = [ct[result] for ct, result in zip(times, behavior_idxs)]
    else:
        behavior_anys = list(map(partial(np.max, axis=1), behavior_results))
        behavior_times = [ct[np.where(idx)] for ct, idx in zip(times, behavior_anys)]

    subtitles = [f'Plot {subtitle}' for subtitle in ['all methods'] + nms]
    fig = plotly_subplots.make_subplots(
        rows=len(nms) + 1, shared_xaxes=True, shared_yaxes=True, subplot_titles=subtitles
    )
    # subplot 1: plot the speed values for all methods
    for t, sp, nm in zip(times, speeds, nms):
        fig.add_trace(
            plotly_go.Scatter(x=t, y=sp, name=nm, mode="lines"),
            row=1, col=1
        )
    # subplot 2,...n: plot the speed values for each individual method
    for i, (behavior, ct, sp, nm) in enumerate(zip(behavior_times, times, speeds, nms)):
        fig.add_trace(
            plotly_go.Scatter(x=ct, y=sp, name=nm, mode="markers"),
            row=i + 2, col=1
        )
        # plot vline at the time of any behavior
        for behavior_at in behavior:
            fig.add_vline(x=behavior_at, row=i + 2, line_color='black')
    # update alpha
    fig.update_traces(opacity=alpha)
    # label
    fig.update_xaxes(title_text='<b>sec</b>', row=len(nms) + 1)
    fig.update_yaxes(title_text='<b>km/h</b>')
    # add title
    if suptitle:
        fig.update_layout(
            title=dict(text=suptitle, font=dict(size=20))
        )

    if save_file_name:
        fig.write_html(save_file_name)
    if show:
        fig.show()
    if browser:
        if isinstance(save_file_name, Path):
            webbrowser.open('file://' + str(save_file_name.absolute()))
        if isinstance(save_file_name, str):
            webbrowser.open('file://' + save_file_name)
    if return_fig:
        return fig


def mpl_comparison_results(
        nms: Tuple[str, ...], times: Tuple[np.ndarray, ...], speeds: Tuple[np.ndarray, ...],
        behavior_results: Tuple[np.ndarray, ...] = None, behavior_idxs: Tuple[np.ndarray, ...] = None,
        suptitle: str = None, figsize: Tuple[float, float] = (20., 10.),
        relative_time: bool = True, alpha: float = 7, save_file_name: Path = None, show: bool = False,
        return_fig: bool = False
):
    """

    Plot the comparison results to test the BBI using plotly

    :param nms: Tuple of names of method to generate subplots
    :param times: Tuple of time for each result
    :param speeds: Tuple of speed for each result
    :param behavior_results: Tuple of behavior result for each result. 4xn shape array, of which columns mean accel, deaccel, start, stop, respectively
    :param suptitle: add supertitle in figure with str value
    :param figsize: figure size
    :param relative_time: normalize the time with start = 0
    :param alpha: the float value for opacity of object in figure
    :param show:
    : browser:
    :param return_fig:
    :param save_file_name: file path to save with html format
    :return: plotly object
    """

    if not isinstance(times[0], np.ndarray):
        times = tuple(map(np.array, times))
    if not isinstance(speeds[0], np.ndarray):
        speeds = tuple(map(np.array, speeds))
    if behavior_results is not None:
        if not isinstance(behavior_results[0], np.ndarray):
            behavior_results = tuple(map(np.array, behavior_results))

    if relative_time:
        times = list(map(lambda t: (t - t[0]) / 1000, times))

    if behavior_idxs is not None:
        behavior_times = [ct[result] for ct, result in zip(times, behavior_idxs)]
    else:
        behavior_anys = list(map(partial(np.max, axis=1), behavior_results))
        behavior_times = [ct[np.where(idx)] for ct, idx in zip(times, behavior_anys)]

    fig, axs = plt.subplots(figsize=figsize, nrows=len(nms) + 1, sharex=True, sharey=True)

    # set subtitles
    subtitles = [f'Plot {subtitle}' for subtitle in ['all methods'] + nms]
    for ax, subtitle in zip(axs, subtitles):
        ax.set_title(subtitle)

    # subplot 1: plot the speed values for all methods
    for t, sp, nm in zip(times, speeds, nms):
        sns.lineplot(x=t, y=sp, label=nm, alpha=alpha, ax=axs[0])
    # subplot 2,...n: plot the speed values for each individual method
    colors = plt.rcParams["axes.prop_cycle"]()
    for i, (behavior, t, sp, nm) in enumerate(zip(behavior_times, times, speeds, nms)):
        sns.scatterplot(x=t, y=sp, label=nm, ax=axs[i + 1], color=next(colors)["color"])
        # plot vline at the time of any behavior
        for behavior_at in behavior:
            axs[i + 1].axvline(x=behavior_at, c='black')

    # label
    # axs[len(nms)+1].set_ylabel('km / h')
    plt.xlabel('sec')
    plt.ylabel('km / h')
    # add title
    if suptitle:
        plt.suptitle(f'{suptitle}', fontweight='bold', fontsize=15)
    if save_file_name:
        plt.savefig(save_file_name)
    if show:
        plt.show(block=False)
    if return_fig:
        return fig

# def figure_plot(plug_time_list, plug_sp_raw_list, maf_result_list, \
#     ref_time_list, ref_sp_list, df_bbi_raw, df_bbi_maf, df_bbi_ref, flag_ref,\
#         User, Date, Trip_Num) :
#     x = 0
#     y = 0
#     for i in range(0, Trip_Num) :
#
#         try :
#             if len(df_bbi_ref[i]) != 0 : flag_ref = True
#             else : flag_ref = False
#         except :
#             flag_ref = False
#
#         if flag_ref == False :
#             fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
#             bbi_time_raw = df_bbi_raw[i].Time
#             axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
#             y_bbi_raw = np.zeros(len(bbi_time_raw))-5
#             axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
#             axes[0].legend()
#             axes[0].grid()
#             axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i+1))
#             axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
#             bbi_time_maf = df_bbi_maf[i].Time
#             y_bbi_maf = np.zeros(len(bbi_time_maf))-5
#             axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
#             axes[1].legend()
#             axes[1].grid()
#             plt.get_current_fig_manager().window.wm_geometry(f"+{x}+{y}")
#         elif flag_ref == True :
#             fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
#             bbi_time_raw = df_bbi_raw[i].Time
#             axes[0].plot(plug_time_list[i], plug_sp_raw_list[i], 'r.', label='plug')
#             y_bbi_raw = np.zeros(len(bbi_time_raw))-5
#             axes[0].plot(bbi_time_raw, y_bbi_raw, '*')
#             axes[0].legend()
#             axes[0].grid()
#             axes[0].set_title(User+' '+str(Date)+'!!!'+ "  Trip No." + str(i+1))
#             axes[1].plot(plug_time_list[i], maf_result_list[i], 'g.', label='ma')
#             bbi_time_maf = df_bbi_maf[i].Time
#             y_bbi_maf = np.zeros(len(bbi_time_maf))-5
#             axes[1].plot(bbi_time_maf, y_bbi_maf, 'b*')
#             axes[1].legend()
#             axes[1].grid()
#
#             bbi_time_and = df_bbi_ref[i].Time
#             axes[2].plot(ref_time_list[i], ref_sp_list[i], 'b.', label='ref')
#             y_bbi_and = np.zeros(len(bbi_time_and))-5
#             axes[2].plot(bbi_time_and, y_bbi_and, '*')
#             axes[2].legend()
#             axes[2].grid()
#             plt.get_current_fig_manager().window.wm_geometry(f"+{x}+{y}")
#         if (i+1)%4== 0 :
#             y += 500
#             x = 0
#         else :
#             x += 500
#
#     plt.show(block=False)
#     while True :
#         num = input("입력 : ")
#         if num == 'c' :
#             plt.close('all')
#             break
#         time.sleep(1)
#
#
