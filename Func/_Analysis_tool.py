from tabulate import tabulate
import folium
from pathlib import Path

def bbi_result_table(bbi_raw_result, bbi_maf_result, bbi_ref_result) : 

    if len(bbi_ref_result) == 0 : 
        x = [["Raw",bbi_raw_result[0],bbi_raw_result[1],
                        bbi_raw_result[2],bbi_raw_result[3]],
            ["MA",bbi_maf_result[0],bbi_maf_result[1],
                        bbi_maf_result[2],bbi_maf_result[3]]]
        print(tabulate(x, headers=["Data", "start", "accel", "stop", "decel"]))
    else : 
        x = [["Raw",bbi_raw_result[0],bbi_raw_result[1],
                        bbi_raw_result[2],bbi_raw_result[3]],
            ["MA",bbi_maf_result[0],bbi_maf_result[1],
                        bbi_maf_result[2],bbi_maf_result[3]],
            ["REF",bbi_ref_result[0],bbi_ref_result[1],
                        bbi_ref_result[2],bbi_ref_result[3]]]
        print(tabulate(x, headers=["Data", "start", "accel", "stop", "decel"]))
        
    
def folium_map(lt_list, ln_list, df_bbi, DATE, User, Comp ) : 
    cPos = [lt_list[0], ln_list[0]]
    myMap = folium.Map(location=cPos,zoom_start=10)
    pos_list = []
    for i in range(0, len(ln_list)) : 
        cPos = [lt_list[i], ln_list[i]]
        pos_list.append(cPos)
        folium.Circle(location = cPos,
                radius = 5,
            ).add_to(myMap)

    #folium.PolyLine(locations=pos_list,tooltip='Polyline').add_to(myMap)  

    for i in range(0, len(df_bbi.Pos)) : 
        cPos = df_bbi.Pos[i]
        cBBI = df_bbi.bbiResult[i]

    if cBBI == 0 : 
        message_bbi = '급출발'
        color_bbi = 'red'
    elif cBBI == 1 : 
        message_bbi = '급가속'
        color_bbi = 'lightblue'
    elif cBBI == 2 : 
        message_bbi = '급정지'
        color_bbi = 'black'
    elif cBBI == 3 : 
        message_bbi = '급감속'
        color_bbi = 'gray'    
        
    folium.Marker(cPos,popup=message_bbi,
                    icon=folium.Icon(color=color_bbi, icon='star')).add_to(myMap)
    
    PROJECT_PATH = Path('.').absolute()
    
    myMap.save(str(PROJECT_PATH)+'/BBI_RESULT/folium/'+str(DATE)+'_'+User+'_'+Comp+'_.html')