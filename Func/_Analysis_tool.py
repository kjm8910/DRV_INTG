from tabulate import tabulate
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