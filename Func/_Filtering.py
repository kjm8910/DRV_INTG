#Speed Noise Filter
import numpy as np


def preprocessing_speed(plug_time_list, plug_sp_list) : 
    for i in range(1, len(plug_sp_list)-10) : 
      
        preSP = plug_sp_list[i-1]
        curSP = plug_sp_list[i]
        dt = (plug_time_list[i] - plug_time_list[i-1])/1000
        del_sp = abs(curSP - preSP)
        
        # 속력 전처리
        # 1. 1개의 데이터만 튀는 경우
        # sp_k - sp_k-1이 15km/h이상 차이가 나지만 sp_k-1과 sp_k+1이의 
        # 차이가 작으면 sp_k = (sp_k-1+sp_k+1)/2로 변경
        if del_sp >= 15 and abs(plug_sp_list[i-1] - plug_sp_list[i+1]) <  5: 
                plug_sp_list[i] = (plug_sp_list[i-1] + plug_sp_list[i+1])/2  
        
        # 2. 속력 편차가 15km/h보다 크고 시간 차분이 2보다 크거나 같으면
        #    preSP를 기준으로 +- 10km/h 차이가 나는 다음 스탭의 속력을 찾아 중간 스탭의 값들을 preSP로 변경
        #    preSP로부터 10초 앞의 데이터까지 찾았는데 찾지 못하면 preSP와 10초 후 데이터를 직선 연결
        if del_sp >= 15 and dt >= 2:
            for j in range(i+1, i + 10) : #i번째는 이미 15키로 차이가 나는 상황이라 볼 필요가 없음
                find_sp = abs(preSP - plug_sp_list[j])
                if find_sp <= 10 : 
                    for k in range(i,j) : 
                        plug_sp_list[k] = plug_sp_list[k-1] + (plug_sp_list[j] - plug_sp_list[i-1])/(j-i)
                    break
                elif j == i+9 : 
                    for k in range(i, i + 10) :
                        plug_sp_list[k] = plug_sp_list[k-1] + (plug_sp_list[i+9] - plug_sp_list[i-1])/10
        
        # 3. 시간 차분이 3초 이상인 경우 앞뒤 5초 데이터를 직선으로 변경
        #if dt >= 3 : 
        #    for k in (i-5, i + 5) :
        #        delta = (plug_sp_list[i+4] - plug_sp_list[i-5])/10
        #        plug_sp_list[k+1] = plug_sp_list[k] + delta
                       
    return plug_sp_list
 
def MovingAverageFilter(plug_time_list, plug_sp_list) :        
    # Moving Average Filter
    N = 2
    cnt_dt = N
    sp_maf_list = np.zeros(len(plug_sp_list))

    del_sp = 1
    dt = 1
    sp_maf_list[0] = plug_sp_list[0]
    for i in range(1, len(plug_sp_list)-N) : 
        cur_SP = plug_sp_list[i]
        #시간 차분 / 속력 차분 계산( 현재 값 - 이전 값)
        if i <= 10 : 
            sp_maf_list[i] = plug_sp_list[i]
            continue
        #else        : 
        #    dt = (plug_time_list[i] - plug_time_list[i-1]) / 1000
        #    del_sp = abs(plug_sp_list[i] - plug_sp_list[i-1])

        # MAF       
        sp_maf = np.mean(plug_sp_list[i:i+N])
        sp_maf_list[i] = sp_maf
        
    sp_maf_list[len(plug_sp_list)-N:] = plug_sp_list[len(plug_sp_list)-N:]
    
    #### BBI 예외처리 #####
    # 0. 초기화
    cnt_skip = 0
    
    # 1. 초반 20초 & 마지막 10초는 BBI 처리 안함
    # 1초부터 20초까지 데이터를 데이터를 20초 데이터로 변경
    # N-19 ~ N(마지막 20초) 데이터를 N-19초 데이터로 변경
    sp_maf_list[0:20] = sp_maf_list[19] 
    sp_maf_list[-20:] = sp_maf_list[-20] 
    for i in range(1, len(sp_maf_list)-14) : 
    
        cTime = plug_time_list[i]
        pTime = plug_time_list[i-1]
        
        curSP = sp_maf_list[i]
        preSP = sp_maf_list[i-1]
      
        #dt = (cTime - pTime )/1000 
        #if dt == 0 : 
        #    dt = 1
        #delV = (curSP - preSP) / dt
        # dt가 2초가 넘는 구간이 있으면 -5초 ~ 10초까지 bbi 평가 안함
        dt_skip = abs(plug_time_list[i+5]-plug_time_list[i+4]) / 1000
        if dt_skip >= 2 : 
            cnt_skip = 14
            sp_maf_list[i] = sp_maf_list[i-1]
            delta_SP = (sp_maf_list[i+14] - sp_maf_list[i])/14
            continue
        elif cnt_skip != 0 : 
            sp_maf_list[i] = sp_maf_list[i-1] + delta_SP
            cnt_skip -= 1
            continue
    
    return sp_maf_list

def func_speed_filter(plug_time_list, plug_sp_list, plug_ac_list) : 
    
    plug_sp_list = preprocessing_speed(plug_time_list, plug_sp_list)
    sp_maf_list = MovingAverageFilter(plug_time_list, plug_sp_list)    
    
    return sp_maf_list