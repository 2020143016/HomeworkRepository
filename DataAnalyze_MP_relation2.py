import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import seaborn as sns

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
#pd.set_option('display.max_columns',None)
#pd.set_option('display.max_rows',None)
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
# MergedData.csv 파일 읽어오기
CON_TIG_ALL = pd.read_csv("MergedData.csv")
#TIG_GDP_correlation 구성
baseColumn = '(TIG)Value'
targetColumn = '(MP)Change(%)'
a = CON_TIG_ALL.columns.tolist().index(baseColumn)
b = CON_TIG_ALL.columns.tolist().index(targetColumn)
TIG_GDP_correlation = pd.DataFrame(CorrelationByNation(CON_TIG_ALL,a,b),columns=['LOCATION','correlation'])
columnName = '(MP)Value'
columnName2 = '(GDPC)Value'
ValueToAdd = pd.DataFrame(OutputMeanValueByNation(columnName),columns=['LOCATION',columnName])
ValueToAdd2 = pd.DataFrame(OutputMeanValueByNation(columnName2),columns=['LOCATION',columnName2])
TIG_GDP_correlation = pd.merge(TIG_GDP_correlation,ValueToAdd,on='LOCATION')
TIG_GDP_correlation = pd.merge(TIG_GDP_correlation,ValueToAdd2,on='LOCATION')
TIG_GDP_correlation['absCorrelation'] = TIG_GDP_correlation['correlation'].abs()
#(GDPC)Value 47000 이하 삭제
idx = TIG_GDP_correlation[TIG_GDP_correlation['(GDPC)Value']<47000].index
TIG_GDP_correlation = TIG_GDP_correlation.drop(idx,axis=0)
print(TIG_GDP_correlation.columns)
print('Correlation: ',calculateCorrelation(TIG_GDP_correlation.to_numpy(),TIG_GDP_correlation.to_numpy(),2,4))
# 그래프 생성
sns.set_theme()
sns.regplot(x=columnName,y='absCorrelation',data=TIG_GDP_correlation,ci=None)
plt.show()

