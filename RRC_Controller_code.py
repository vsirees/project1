# importing library's
import pandas as pd
import numpy as np
import glob

#local path
path = r'C:\Users\siriv\OneDrive\Desktop\project1\files'

#importing files
files = glob.glob(path + "/*.csv")

#appending files
df1 = []
for filename in files:
    df1.append(pd.read_csv(filename))

df1 = pd.concat(df1, ignore_index=True)

# file import
df = pd.read_csv(r"C:\Users\siriv\OneDrive\Desktop\project1\S22_MOBILITY_DL_ITER5_v1.csv")

# droping null values
df1=df.dropna(subset=['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number'])

# changing data types
df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number'].astype('int')
df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell Slot Number']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell Slot Number'].astype('int')

# current_frameslot calculation
df1['current_frameslot']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number'].astype('str')+df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell Slot Number'].astype('str')

#previous_frameslot calculation
df1['previous_frameslot']=df1['current_frameslot'].shift(1)

# filling missing values with zero
df1['previous_frameslot']=df1['previous_frameslot'].fillna(0)

# delta calculation
df1['delta']=df1['current_frameslot'].astype('int')-df1['previous_frameslot'].astype('int')
df1['Continious_Activity_Tx']=np.where(df1['delta']==1,df1['delta']+1,df1['delta'])
df1['Continious Tx_Off']=np.where(df1['delta']>1,df1['current_frameslot'].astype('int')-df1['previous_frameslot'].astype('int'),df1['delta'])


#creating new column "previous_system_frame_number"
df1['previous_system_frame_number']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number'].shift(1)

#creating new column "current_system_frame_number"
df1['current_system_frame_number']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell System Frame Number'].shift(0)

#filling missing values with zero
df1['current_system_frame_number']=df1['current_system_frame_number'].fillna(0).astype('int')
df1['previous_system_frame_number']=df1['previous_system_frame_number'].fillna(0).astype('int')

#checking data types
df1.dtypes

#applying condition " current line system frame number is less then previous system frame number "
df1['system_frame_number'] =np.where(df1['current_sys	tem_frame_number'] <= df1['previous_system_frame_number'],1,0)

#calculation
df1["SCS_column"]=np.where((df1["system_frame_number"]==1) & 
                           (df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="15kHz"),
                           (10239-df1["previous_frameslot"].astype('int')+df1["current_frameslot"].astype('int')),df1["system_frame_number"])

#calculation
df1["SCS_column"]=np.where((df1["system_frame_number"]==1) & 
                           (df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="30kHz"),
                           (102319-df1["previous_frameslot"].astype('int')+df1["current_frameslot"].astype('int')),df1["system_frame_number"])


#calculation
df1["SCS_column"]=np.where((df1["system_frame_number"]==1) & 
                           (df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="120kHz"),
                           (102379-df1["previous_frameslot"].astype('int')+df1["current_frameslot"].astype('int')),df1["system_frame_number"])


#exporting file
df1.to_csv(r"C:\Users\siriv\OneDrive\Desktop\project1\S22_MOBILITY_DL_ITER5_v1.csv",index=True)


# current_slot_number_column
df1['current_slot_number']=df1['Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell Slot Number'].shift(0)

# previous_slot_number_column
df1['previous_slot_number']=df1['current_slot_number'].shift(1)

#filling missing values with zero
df1['current_slot_number']=df1['current_slot_number'].fillna(0).astype('int')
df1['previous_slot_number']=df1['previous_slot_number'].fillna(0).astype('int')


#current & previous slot numbers difference
df1['slot_number_diff']=df1['current_slot_number']-df1['previous_slot_number']

#calculation
df1["slot_number"]=np.where(df1["slot_number_diff"]<=9&(df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="15kHz"),1,0)
df1["slot_number"]=np.where(df1["slot_number_diff"]<=19&(df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="30kHz"),1,0)
df1["slot_number"]=np.where(df1["slot_number_diff"]<=79&(df1["Qualcomm 5G-NR MAC UL Physical Channel Schedule Report[Per Slot] PCell SCS"]=="120kHz"),1,0)
				   

















