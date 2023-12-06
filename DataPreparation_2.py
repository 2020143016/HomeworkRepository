import numpy as np
import pandas as pd
import math

# 불필요한 columns 제거('LOCATION_y','TIME_y','L/T') return pandasDataframe
def dropDuplicatedColumns(DF):
    lst = ['LOCATION_y','TIME_y','L/T']
    PDD = DF.drop(lst,axis=1)
    return PDD
# 불필요한 columns 제거('LOCATION_y','TIME_y') return pandasDataframe
def dropDuplicatedColumnsExceptLt(DF):
    lst = ['LOCATION_y','TIME_y']
    PDD = DF.drop(lst,axis=1)
    return PDD
# Base 와 target의 correlation을 구함 return float
def calculateCorrelation(base,target,baseColumn,targetColumn):# textfileExceptions 108p base: numpy / target: numpy
    sum_base_vals = sum_target_vals = 0
    sum_base_sqrd = sum_target_sqrd = 0
    sum_product = 0

    num_values = len(base.tolist())

    for i in range(0,num_values):
        sum_base_vals = sum_base_vals + float(base[i][baseColumn]) # 1은 나중에 바꿀것
        sum_target_vals = sum_target_vals + float(target[i][targetColumn])
        sum_base_sqrd = sum_base_sqrd+float(base[i][baseColumn])**2
        sum_target_sqrd = sum_target_sqrd+float(target[i][targetColumn])**2
        sum_product = sum_product + float(base[i][baseColumn])*float(target[i][targetColumn])

        #calculate and display correlation value
    numer = (num_values*sum_product) - (sum_base_vals*sum_target_vals)

    denom = math.sqrt(abs(((num_values*sum_base_sqrd)-(sum_base_vals**2))*((num_values*sum_target_sqrd)-(sum_target_vals**2))))
    return numer/denom
#numpy 형의 데이터 입력시 [0]의 'LOCATION'에 포함된 요소 리스트 출력 return tuple(list,len(list))
def CountryExtractor(ListToExtract):# return(list of country, number of country included)
    ListOfCountry = []
    for i in range(len(ListToExtract)):
        if not(ListToExtract[i][0] in ListOfCountry):
            ListOfCountry.append(ListToExtract[i][0])
    return (ListOfCountry,len(ListOfCountry))
# LOCATION 별 column1과 column2의 correlation을 출력 return lst(2d)
def CorrelationByNation(inputData,column1,column2):
    DataToShowCorrelation = inputData
    lstOfLocation = CountryExtractor(DataToShowCorrelation.to_numpy())[0]
    lst = []
    for i in range(len(lstOfLocation)):
        base = DataToShowCorrelation[DataToShowCorrelation['LOCATION']==CountryExtractor(DataToShowCorrelation.to_numpy())[0][i]]
        target = DataToShowCorrelation[DataToShowCorrelation['LOCATION']==CountryExtractor(DataToShowCorrelation.to_numpy())[0][i]]
        basecolumn = column1
        targetcolumn = column2
        lst.append([lstOfLocation[i],calculateCorrelation(base.to_numpy(),target.to_numpy(),basecolumn,targetcolumn)])
    return lst
# LOCATION 별 targetColumnName에 해당하는 평균을 출력 return lst(2d)
def OutputMeanValueByNation(targetColumnName):
    df = CON_TIG_ALL
    df['NewMeanValue'] = df.groupby(['LOCATION'])[targetColumnName].transform('mean')
    df= df.drop_duplicates(['LOCATION'])
    targetIndex = df.columns.tolist().index('NewMeanValue')
    #print(df)
    df_np = df.to_numpy()
    lst = []
    lstOfLocation = CountryExtractor(df.to_numpy())[0]
    for i in range(len(lstOfLocation)):
        if lstOfLocation[i] == df_np[i][0]:
            lst.append([lstOfLocation[i], df_np[i][targetIndex]])
    return lst

# 전처리 한 데이터 변수에 할당
TIG_pd = pd.read_csv('ProcessingDataset_Trust_in_government.csv')
MP_pd = pd.read_csv('ProcessingDataset_Multifactor_productivity.csv')
PLI_pd = pd.read_csv('ProcessingDataset_Price_level_indices.csv')
GDP_pd = pd.read_csv('ProcessingDataset_Gross_domestic_product.csv')
GDPCAP_pd = pd.read_csv('ProcessingDataset_Gross_domestic_productCAP.csv')

# 데이터별 추가로 필요한 데이터 생성
TIG_pd['Mean by TIME'] = TIG_pd.groupby(['TIME'])['Value'].transform('mean') # mean value of data in same year
TIG_pd['std by TIME'] = TIG_pd.groupby(['TIME'])['Value'].transform('std') # std value of data in same year
TIG_pd['SND by TIME'] = (TIG_pd['Value']-TIG_pd['Mean by TIME'])/TIG_pd['std by TIME'] # Standard Normal Distribution value of data in same year
GDP_pd['Mean of Change(%) by TIME'] = GDP_pd.groupby(['TIME'])['Change of Value(%)'].transform('mean')
GDP_pd['std of Change(%) by TIME'] = GDP_pd.groupby(['TIME'])['Change of Value(%)'].transform('std')
GDP_pd['SND of Change(%) by TIME'] = (GDP_pd['Change of Value(%)']-GDP_pd['Mean of Change(%) by TIME'])/GDP_pd['std of Change(%) by TIME']
GDPCAP_pd['Mean of Change(%) by TIME'] = GDPCAP_pd.groupby(['TIME'])['Change of Value(%)'].transform('mean')
GDPCAP_pd['std of Change(%) by TIME'] = GDPCAP_pd.groupby(['TIME'])['Change of Value(%)'].transform('std')
GDPCAP_pd['SND of Change(%) by TIME'] = (GDPCAP_pd['Change of Value(%)']-GDPCAP_pd['Mean of Change(%) by TIME'])/GDPCAP_pd['std of Change(%) by TIME']

#데이터를 merge 했을 때 값을 구분할 수 있도록 columns rename
TIG_pd.rename(columns={'Value':'(TIG)Value','Mean by TIME':'(TIG)MbT','std by TIME':'(TIG)sbT','SND by TIME':'(TIG)SND by TIME'},inplace = True)
MP_pd.rename(columns={'Value':'(MP)Value','Change of Value(%)':'(MP)Change(%)'},inplace = True)
PLI_pd.rename(columns={'Value':'(PLI)Value'},inplace = True)
GDP_pd.rename(columns={'Value':'(GDP)Value','Change of Value(%)':'(GDP)Change(%)'},inplace = True)
GDPCAP_pd.rename(columns={'Value':'(GDPC)Value','Change of Value(%)':'(GDPC)Change(%)','Mean of Change(%) by time':'(GDPC)Mean of Change(%) by time',
},inplace = True)

# LOCATION과 TIME 동시에 나타내는 column 만들기
TIG_pd['L/T'] = TIG_pd['LOCATION'].astype('str') + '/' + TIG_pd['TIME'].astype('str')
MP_pd['L/T'] = MP_pd['LOCATION'].astype('str') + '/' + MP_pd['TIME'].astype('str')
PLI_pd['L/T'] = PLI_pd['LOCATION'].astype('str') + '/' + PLI_pd['TIME'].astype('str')
GDP_pd['L/T'] = GDP_pd['LOCATION'].astype('str') + '/' + GDP_pd['TIME'].astype('str')
GDPCAP_pd['L/T'] = GDPCAP_pd['LOCATION'].astype('str') + '/' + GDPCAP_pd['TIME'].astype('str')

# 정부 신뢰도(TIG)와 다른 지표를 LOCATION과 TIME 기준으로 합쳐 정부신뢰도와 그외 데이터가 병합된 데이터프레임 생성(CON_TIG_XXX)
CON_TIG_MP = pd.merge(TIG_pd,MP_pd,on='L/T')
CON_TIG_PLI = pd.merge(TIG_pd,PLI_pd,on='L/T')
CON_TIG_GDP = pd.merge(TIG_pd,GDP_pd,on='L/T')
CON_TIG_GDP_CAP = pd.merge(TIG_pd,GDPCAP_pd,on='L/T')
# 모든 데이터 합친 데이터프레임생성
CON_TIG_ALL = pd.merge(TIG_pd,PLI_pd,on='L/T')
CON_TIG_ALL = dropDuplicatedColumnsExceptLt(CON_TIG_ALL)
CON_TIG_ALL = pd.merge(CON_TIG_ALL,GDP_pd,on='L/T')
CON_TIG_ALL.rename(columns={'LOCATION':'LOCATION_y','TIME':'TIME_y','LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_ALL = dropDuplicatedColumnsExceptLt(CON_TIG_ALL)
CON_TIG_ALL = pd.merge(CON_TIG_ALL,GDPCAP_pd,on='L/T')
CON_TIG_ALL.rename(columns={'LOCATION':'LOCATION_y','TIME':'TIME_y','LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_ALL = dropDuplicatedColumnsExceptLt(CON_TIG_ALL)
CON_TIG_ALL = pd.merge(CON_TIG_ALL,MP_pd,on='L/T')
CON_TIG_ALL = dropDuplicatedColumns(CON_TIG_ALL)

# 불필요한 요소 삭제, rename
CON_TIG_MP.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_PLI.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_GDP.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_GDP_CAP.rename(columns={'LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
CON_TIG_MP = dropDuplicatedColumns(CON_TIG_MP)
CON_TIG_PLI = dropDuplicatedColumns(CON_TIG_PLI)
CON_TIG_GDP = dropDuplicatedColumns(CON_TIG_GDP)
CON_TIG_GDP_CAP = dropDuplicatedColumns(CON_TIG_GDP_CAP)
CON_TIG_ALL.rename(columns={'Mean of Change(%) by TIME_x':'(GDP)Mean of Change(%) by TIME', 'std of Change(%) by TIME_x':'(GDP)std of Change(%) by TIME',
       'SND of Change(%) by TIME_x':'(GDP)SND of Change(%) by TIME',
       'Mean of Change(%) by TIME_y':'(GDPC)Mean of Change(%) by TIME', 'std of Change(%) by TIME_y':'(GDPC)std of Change(%) by TIME',
       'SND of Change(%) by TIME_y':'(GDPC)SND of Change(%) by TIME','LOCATION_x':'LOCATION','TIME_x':'TIME'},inplace = True)
# 모든 데이터 합친 데이터프레임 csv파일로 저장
CON_TIG_ALL.to_csv("MergedData.csv",mode='w',index=False)