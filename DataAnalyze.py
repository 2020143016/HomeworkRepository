import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# plt showing
'''
df1 = pd.read_csv('ProcessingDataset_Trust_in_government.csv')
value = df1.loc[df1['LOCATION']=='AUS']['Value']
year = df1.loc[df1['LOCATION']=='AUS']['TIME']
dif,ax = plt.subplots()
ax.scatter(year,value)
print(df1.loc[df1['LOCATION']=='AUS'])
plt.show()
'''
# 불필요한 columns 제거('LOCATION_y','TIME_y','L/T')
def dropDuplicatedColumns(DF):
    lst = ['LOCATION_y','TIME_y','L/T']
    PDD = DF.drop(lst,axis=1)
    return PDD
# 전처리 한 데이터 변수에 할당
TIG_pd = pd.read_csv('ProcessingDataset_Trust_in_government.csv')
MP_pd = pd.read_csv('ProcessingDataset_Multifactor_productivity.csv')
PLI_pd = pd.read_csv('ProcessingDataset_Price_level_indices.csv')
GDP_pd = pd.read_csv('ProcessingDataset_Gross_domestic_product.csv')

# 데이터별 추가로 필요한 데이터 생성
TIG_pd['Mean by TIME'] = TIG_pd.groupby(['TIME'])['Value'].transform('mean') # mean value of data in same year
TIG_pd['std by TIME'] = TIG_pd.groupby(['TIME'])['Value'].transform('std') # std value of data in same year
TIG_pd['SND by TIME'] = (TIG_pd['Value']-TIG_pd['Mean by TIME'])/TIG_pd['std by TIME'] # Standard Normal Distribution value of data in same year

#데이터를 merge 했을 때 값을 구분할 수 있도록 columns rename
TIG_pd.rename(columns={'Value':'Value=T','Mean by TIME':'MbT=T','std by TIME':'sbT=T','SND by TIME':'SbT=T'},inplace = True)
MP_pd.rename(columns={'Value':'Value=M','Change of Value(%)':'Change(%)=M'},inplace = True)
PLI_pd.rename(columns={'Value':'Value=P'},inplace = True)
GDP_pd.rename(columns={'Value':'Value=G','Change of Value(%)':'Change(%)=G'},inplace = True)

#LOCATION과 TIME 동시에 나타내는 column 만들기
TIG_pd['L/T'] = TIG_pd['LOCATION'].astype('str') + '/' + TIG_pd['TIME'].astype('str')
MP_pd['L/T'] = MP_pd['LOCATION'].astype('str') + '/' + MP_pd['TIME'].astype('str')
PLI_pd['L/T'] = PLI_pd['LOCATION'].astype('str') + '/' + PLI_pd['TIME'].astype('str')
GDP_pd['L/T'] = GDP_pd['LOCATION'].astype('str') + '/' + GDP_pd['TIME'].astype('str')
#정부 신뢰도와 다른 지표 함치기
CON_TIG_MP = pd.merge(TIG_pd,MP_pd,on='L/T')
CON_TIG_PLI = pd.merge(TIG_pd,PLI_pd,on='L/T')
CON_TIG_GDP = pd.merge(TIG_pd,GDP_pd,on='L/T')
#불필요한 요소 삭제, rename
CON_TIG_MP.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_PLI.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_GDP.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_MP = dropDuplicatedColumns(CON_TIG_MP)
CON_TIG_PLI = dropDuplicatedColumns(CON_TIG_PLI)
CON_TIG_GDP = dropDuplicatedColumns(CON_TIG_GDP)

print(CON_TIG_MP)
print(CON_TIG_PLI)
print(CON_TIG_GDP)

