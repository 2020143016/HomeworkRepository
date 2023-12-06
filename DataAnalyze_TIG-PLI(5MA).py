import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
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

CON_TIG_ALL = pd.read_csv("MergedData.csv")
CON_TIG_ALL['abs(PLI)Value-5MA'] = ((CON_TIG_ALL['(PLI)Value'] - CON_TIG_ALL['(PLI)5MA'])**2)**(1/2)

# 그래프 생성
columnName_x = '(TIG)Value'
columnName_y = 'abs(PLI)Value-5MA'
x = CON_TIG_ALL[columnName_x]
y = CON_TIG_ALL[columnName_y]
dif,ax = plt.subplots()
ax.scatter(x,y)
ax.set_xlabel(columnName_x)
ax.set_ylabel(columnName_y)
plt.show()

