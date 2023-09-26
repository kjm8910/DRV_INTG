## Module Define
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
def bbi_detection_no_exception(time_list, sp_list, ln_list, lt_list) : 
    
    bbi_result = np.zeros([4])
    #1 : 급출발, 2: 급가속, 3 : 급정지, 4 : 급감속
    
    preSP   = 0
    pTime   = 0
    cTime   = 0
    dt      = 1
    time_bbi_list = []
    pos_bbi_list = []
    bbi_result_list = []
    
    for i in range(1, len(sp_list)) : 
        
        cTime = time_list[i]
        pTime = time_list[i-1]
        cPos = [lt_list[i], ln_list[i]]
        curSP = sp_list[i]
        preSP = sp_list[i-1]
      
        dt = (cTime - pTime )/1000 
        if dt == 0 : dt = 1
        delV = (curSP - preSP) / dt
                
        # 1. 급출발
        if preSP <= 5 and delV >= 10 : 
            bbi_result[0] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 0]
            bbi_result_list.append(result)
            continue
            
        # 2. 급가속
        if preSP > 5 and preSP <= 10 and delV >= 12 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 1]
            bbi_result_list.append(result)
            continue
        elif preSP > 10 and preSP <= 20 and delV >= 10 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 1]
            bbi_result_list.append(result)
            continue
        elif preSP > 20 and delV >= 8 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 1]
            bbi_result_list.append(result)
            continue
            
        # 3. 급정지
        if delV  <= -14 and curSP < 5 : 
            bbi_result[2] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 2]
            bbi_result_list.append(result)
            continue
        # 4. 급감속
        if preSP <= 30 and delV <= -14 and curSP >= 5 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 3]
            bbi_result_list.append(result)
            continue
        elif preSP <= 50 and delV <= -15 and curSP >= 6 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 3]
            bbi_result_list.append(result)
            continue
        elif preSP > 50 and delV <= -15 and curSP >= 6 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            pos_bbi_list.append(cPos)
            result = [cTime, cPos, 3]
            bbi_result_list.append(result)
            continue
    df = DataFrame(bbi_result_list, columns=['Time','Pos','bbiResult'])        
    return df, bbi_result
        
    
def bbi_detection_v001(time_list, sp_list) : 
    
    bbi_result = np.zeros([4])
    #1 : 급출발, 2: 급가속, 3 : 급정지, 4 : 급감속
    
    preSP   = 0
    pTime   = 0
    cTime   = 0
    dt      = 1
    time_bbi_list = []
    cnt_skip = 0
    
    for i in range(2, len(sp_list)-10) : 
        
        cTime = time_list[i]
        pTime = time_list[i-1]
        
        curSP = sp_list[i]
        preSP = sp_list[i-1]
      
        dt = (cTime - pTime )/1000 
        delV = (curSP - preSP) / dt
        
        #fisrt_SP = sp_list[i]
        delV_2sec = np.average(np.diff(sp_list[i-1:i+2]))
        delV_3sec = np.average(np.diff(sp_list[i-1:i+3]))
        delV_5sec = np.average(np.diff(sp_list[i-1:i+5]))
        # 초반 10초는 평가 안함
        if i < 10 : 
            continue
        
        # dt가 2초가 넘는 구간이 있으면 -5초 ~ 10초까지 bbi 평가 안함
        dt_skip = abs(time_list[i+6]-time_list[i+5]) / 1000
        if dt_skip >= 2 or dt_skip == 0: 
            cnt_skip = 15
            continue
        elif cnt_skip!= 0 : 
            cnt_skip -= 1
            continue
   
        # 1. 급출발
        #if curSP < 6 and delV_2sec >= 10 : # 
        #    bbi_result[0] += 1
        #    time_bbi_list.append(cTime)
        #    continue
        if preSP <= 6 and delV_5sec >= 8 : #delV_2sec >= 9
            bbi_result[0] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 3
            continue
        
            
        # 2. 급가속
        if curSP >= 6 and curSP <= 10 and delV_2sec >= 10 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        elif curSP > 10 and curSP <= 20 and delV_2sec >= 10 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        elif curSP > 20 and delV_2sec >= 7 : 
            bbi_result[1] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        
        # 3. 급정지
        fSP_2sec = sp_list[i+1]
        if delV_2sec  <= -10 and fSP_2sec <= 6 : 
            bbi_result[2] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        
        # 4. 급감속
        if preSP <= 30 and delV_2sec <= -12 and fSP_2sec >= 6 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        elif preSP <= 50 and delV_2sec <= -13 and fSP_2sec >= 6 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
        elif preSP > 50 and delV_2sec <= -13 and fSP_2sec >= 6 : 
            bbi_result[3] += 1
            time_bbi_list.append(cTime)
            cnt_skip = 2
            continue
            
    return bbi_result, time_bbi_list

def count_dt_over(plug_time_list) : 
    dt_list = np.diff(plug_time_list)/1000
    mask = (dt_list >= 2)
    num_dt_over = len(dt_list[mask])
    return num_dt_over