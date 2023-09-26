
import folium
from folium import plugins
import datetime
import numpy as np

# raw speed vs filter speed
def draw_map(plug_lt_list,plug_ln_list, plug_time_list, plug_sp_raw_list, sp_maf_list, df_raw_bbi, df_maf_bbi) :
    center = [plug_lt_list[0],plug_ln_list[0]]
    locations = list(zip(plug_lt_list,plug_ln_list))
    m = folium.plugins.DualMap(location=center,zoom_start=10)
    features = ['rapid_accel_taxi_gps', 'rapid_deaccel_taxi_gps', 'sudden_start_taxi_gps','sudden_stop_taxi_gps']
    folium.PolyLine( locations = locations, color="#993399", weight=10, opacity=0.5, line_opacity=0.3, ).add_to(m.m1)
    folium.PolyLine( locations = locations, color="#993399", weight=10, opacity=0.5, line_opacity=0.3, ).add_to(m.m2)

    for i, (sp_raw,time,lt,ln,filter_sp) in enumerate(zip(plug_sp_raw_list,plug_time_list,plug_lt_list,plug_ln_list,sp_maf_list)):    
        d_time = datetime.datetime.fromtimestamp(time//1000).strftime('%Y-%m-%d %H:%M:%S')
        tooltip = ( f"ct: {time}<br>"
                    f"시간: {d_time}<br>"
                    f"lat: {lt}<br>"
                    f"lon: {ln}<br>"
                    f"gps 속력: {sp_raw}<br>"
                    f"filter gps 속력: {filter_sp}<br>"
                   )
        if not i:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon='home', color='black'), popup="Start", tooltip=tooltip
            ).add_to(m.m1)
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon='home', color='black'), popup="Start", tooltip=tooltip
            ).add_to(m.m2)

        elif i == len(locations) - 1:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon = 'flag', color='black'), popup="End", tooltip=tooltip
            ).add_to(m.m1)
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon = 'flag', color='black'), popup="End", tooltip=tooltip
            ).add_to(m.m2)
        else:
            folium.CircleMarker( location=(lt,ln), radius=3, color='blue', tooltip=tooltip
            ).add_to(m.m1)
            folium.CircleMarker( location=(lt,ln), radius=3, color='blue', tooltip=tooltip
            ).add_to(m.m2)
        
    color_list = ['red','blue','darkpurple','lightgreen']
    bbi_list = ['start','accel','stop','decel']
    for i in range(len(df_raw_bbi)):
        folium.Marker( location=[df_raw_bbi.iloc[i]['Pos']][0], icon=folium.Icon(icon='star', color=color_list[df_raw_bbi.iloc[i]['bbiResult']]), popup=bbi_list[df_raw_bbi.iloc[i]['bbiResult']], tooltip=tooltip
        ).add_to(m.m1)
    for j in range(len(df_maf_bbi)):
        folium.Marker( location=[df_maf_bbi.iloc[j]['Pos']][0], icon=folium.Icon(icon='star', color=color_list[df_maf_bbi.iloc[j]['bbiResult']]), popup=bbi_list[df_maf_bbi.iloc[j]['bbiResult']], tooltip=tooltip
        ).add_to(m.m2)
        
    # save_path = './result.html'
    # m.save( save_path )
    return m

def draw_map_rtk(plug_lt_list,plug_ln_list, plug_time_list, plug_sp_raw_list, sp_maf_list, df_raw_bbi, df_maf_bbi, ref_lt_list, ref_ln_list, ref_time_list, ref_sp_list, df_ref_bbi):
    center = [plug_lt_list[0],plug_ln_list[0]]
    locations = list(zip(plug_lt_list,plug_ln_list))
    center_ref = [ref_lt_list[0],ref_ln_list[0]]
    locations_ref = list(zip(ref_lt_list,ref_ln_list))
    m = folium.plugins.DualMap(location=center,zoom_start=10)
    features = ['rapid_accel_taxi_gps', 'rapid_deaccel_taxi_gps', 'sudden_start_taxi_gps','sudden_stop_taxi_gps']
    folium.PolyLine( locations = locations, color="#993399", weight=10, opacity=0.5, line_opacity=0.3, ).add_to(m.m1)
    folium.PolyLine( locations = locations_ref, color="#993399", weight=10, opacity=0.5, line_opacity=0.3, ).add_to(m.m2)

    for i, (time, sp_raw,filter_sp, lt,ln,) in enumerate(zip(plug_time_list, plug_sp_raw_list,sp_maf_list ,plug_lt_list,plug_ln_list)):    
        d_time = datetime.datetime.fromtimestamp(time//1000).strftime('%Y-%m-%d %H:%M:%S')
        tooltip = ( f"ct: {time}<br>"
                    f"시간: {d_time}<br>"
                    f"lat: {lt}<br>"
                    f"lon: {ln}<br>"
                    f"gps 속력: {sp_raw}<br>"
                    f"filter gps 속력: {filter_sp}<br>"
                   )
        if not i:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon='home', color='black'), popup="Start", tooltip=tooltip
            ).add_to(m.m1)
        elif i == len(locations) - 1:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon = 'flag', color='black'), popup="End", tooltip=tooltip
            ).add_to(m.m1)
        else:
            folium.CircleMarker( location=(lt,ln), radius=3, color='blue', tooltip=tooltip
            ).add_to(m.m1)
            
    for i, (time, sp_raw, lt,ln,) in enumerate(zip(ref_time_list, ref_sp_list ,ref_lt_list,ref_ln_list)):    
        d_time = datetime.datetime.fromtimestamp(time//1000).strftime('%Y-%m-%d %H:%M:%S')
        tooltip = ( f"ct: {time}<br>"
                    f"시간: {d_time}<br>"
                    f"lat: {lt}<br>"
                    f"lon: {ln}<br>"
                    f"gps 속력: {sp_raw}<br>"
                   )
        if not i:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon='home', color='black'), popup="Start", tooltip=tooltip
            ).add_to(m.m2)
        elif i == len(locations) - 1:
            folium.Marker( location=(lt,ln), icon=folium.Icon(icon = 'flag', color='black'), popup="End", tooltip=tooltip
            ).add_to(m.m2)
        else:
            folium.CircleMarker( location=(lt,ln), radius=3, color='blue', tooltip=tooltip
            ).add_to(m.m2)
        
    color_list = ['red','blue','darkpurple','lightgreen']
    bbi_list = ['start','accel','stop','decel']
    for i in range(len(df_raw_bbi)):
        folium.Marker( location=[df_raw_bbi.iloc[i]['Pos']][0], icon=folium.Icon(icon='star', color=color_list[df_raw_bbi.iloc[i]['bbiResult']]), popup=bbi_list[df_raw_bbi.iloc[i]['bbiResult']], tooltip=tooltip
        ).add_to(m.m1)
    for j in range(len(df_ref_bbi)):
        folium.Marker( location=[df_ref_bbi.iloc[j]['Pos']][0], icon=folium.Icon(icon='star', color=color_list[df_ref_bbi.iloc[j]['bbiResult']]), popup=bbi_list[df_ref_bbi.iloc[j]['bbiResult']], tooltip=tooltip
        ).add_to(m.m2)
        
    # save_path = './result_ref.html'
    # m.save( save_path )
    return m