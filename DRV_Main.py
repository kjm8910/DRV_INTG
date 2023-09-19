#### Module Define ######################################
from Func._Main_Func import * 
#### 0. 초기값 입력 ########################################
# a. 분석할 날짜
#   [0] : Start Date / [1] End Date
Date_List = ['20230910', '20230917']
# b. User List
User_List = ['Zed']
# c. Plug type List
Plug_List = ['lux1']
# d. Simulation Mode Type
#   0 : User, 1 : Plug, ( 2 : User & Plug X)
SimMode = 0

#### 3.Simulation Start ##################################
Start_Simulation(SimMode, Date_List, User_List, Plug_List)

