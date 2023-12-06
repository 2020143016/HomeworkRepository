#python version 3.9.12 64bit
import numpy as np
import pandas as pd
# LOCATION 값을 출력
def CountryExtractor(ListToExtract):
    ListOfCountry = []
    for i in range(len(ListToExtract)):
        if not(ListToExtract[i][0] in ListOfCountry):
            ListOfCountry.append(ListToExtract[i][0])
    return (ListOfCountry,len(ListOfCountry))
# TrustInGovernment에서와 동시에 존재하는 LOCATION 출력
def ExtractSameCountry(Target_list):
    lst = []
    for i in CountryExtractor(csv_TrustInGovernment_np)[0]:
        if i in CountryExtractor(Target_list)[0]:
            lst.append(i)
    return lst
#쓰지 않는 열 삭제
def DataProcessing(PandasData):
    lst = ['LOCATION','TIME','Value','Change of Value(%)','(PLI)5MA']
    lstOfColumns = []
    for i in range(len(PandasData.columns)):
        if not(PandasData.columns[i] in lst):
            lstOfColumns.append(PandasData.columns[i])
    PDD = PandasData.drop(lstOfColumns,axis=1)
    return PDD
# 2006~2022 밖의 시간대 이거나 TrustInGovernment에 존재하지 않는 LOCATION을 갖는 행들을 삭제
def EraseNotUsableData(PandasData):
    idx = PandasData[~(PandasData['LOCATION'].isin(TIG_Country))|((PandasData['TIME'].astype('int')>2022) | (PandasData['TIME'].astype('int')<2006))].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
# MEASURE 가 AGRWTH인 행 삭제
def EraseNotUsingDataForMP(PandasData):
    idx = PandasData[PandasData['MEASURE'].astype('str') == 'AGRWTH'].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
# MEASURE 가 USD_CAP인 행 삭제
def EraseNotUsingDataForGDP(PandasData):
    idx = PandasData[PandasData['MEASURE'].astype('str') == 'USD_CAP'].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
# MEASURE 가 MLN_USD인 행 삭제
def EraseNotUsingDataForGDPCAP(PandasData):
    idx = PandasData[PandasData['MEASURE'].astype('str') == 'MLN_USD'].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
#csv 데이터 불러오기
csv_TrustInGovernment = pd.read_csv("Dataset_Trust_in_government.csv")
csv_MultifactorProductivity = pd.read_csv("Dataset_Multifactor_productivity.csv")
csv_GrossDomesticProduct = pd.read_csv("Dataset_Gross_domestic_product.csv")
csv_GrossDomesticProductCAP = pd.read_csv("Dataset_Gross_domestic_product.csv")
csv_PriceLevelIndices = pd.read_csv("Dataset_Price_level_indices.csv")
csv_MultifactorProductivity = EraseNotUsingDataForMP(csv_MultifactorProductivity)
csv_GrossDomesticProduct = EraseNotUsingDataForGDP(csv_GrossDomesticProduct)
csv_GrossDomesticProductCAP = EraseNotUsingDataForGDPCAP(csv_GrossDomesticProductCAP)

# 데이터별 필요한 행 추가
csv_PriceLevelIndices['(PLI)5MA'] = csv_PriceLevelIndices['Value'].rolling(window=5).mean()
csv_GrossDomesticProduct['Data before available'] = np.where(csv_GrossDomesticProduct['TIME'].shift() == csv_GrossDomesticProduct['TIME']-1,1,0)
csv_MultifactorProductivity['Data before available'] = np.where(csv_MultifactorProductivity['TIME'].shift() == csv_MultifactorProductivity['TIME']-1,1,0)
csv_GrossDomesticProduct['Change of Value(%)'] = 100*csv_GrossDomesticProduct['Data before available']*(csv_GrossDomesticProduct['Value'] - csv_GrossDomesticProduct['Value'].shift(1))/csv_GrossDomesticProduct['Value'].shift(1)
csv_MultifactorProductivity['Change of Value(%)'] = 100*csv_MultifactorProductivity['Data before available']*(csv_MultifactorProductivity['Value'] - csv_MultifactorProductivity['Value'].shift(1))/csv_MultifactorProductivity['Value'].shift(1)
csv_GrossDomesticProductCAP['Data before available'] = np.where(csv_GrossDomesticProductCAP['TIME'].shift() == csv_GrossDomesticProductCAP['TIME']-1,1,0)
csv_GrossDomesticProductCAP['Change of Value(%)'] = 100*csv_GrossDomesticProductCAP['Data before available']*(csv_GrossDomesticProductCAP['Value'] - csv_GrossDomesticProductCAP['Value'].shift(1))/csv_GrossDomesticProductCAP['Value'].shift(1)

# pandas 를 numpy로
csv_TrustInGovernment_np = csv_TrustInGovernment.to_numpy()
csv_MultifactorProductivity_np = csv_MultifactorProductivity.to_numpy()
csv_GrossDomesticProduct_np = csv_GrossDomesticProduct.to_numpy()
csv_PriceLevelIndices_np = csv_PriceLevelIndices.to_numpy()
csv_GrossDomesticProductCAP_np = csv_GrossDomesticProductCAP.to_numpy()

# 데이터별 존제하는 LOCATION list 변수에 할당
TIG_Country = CountryExtractor(csv_TrustInGovernment_np)[0]
MP_Contry = CountryExtractor(csv_MultifactorProductivity_np)[0]
GDP_Country = CountryExtractor(csv_GrossDomesticProduct_np)[0]
PLI_Country = CountryExtractor(csv_PriceLevelIndices_np)[0]
GDPCAP_Country = CountryExtractor(csv_GrossDomesticProductCAP_np)[0]

# 필요하지 않은 열과 행 삭제
TIG_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_TrustInGovernment))
MP_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_MultifactorProductivity))
GDP_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_GrossDomesticProduct))
PLI_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_PriceLevelIndices))
GDPCAP_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_GrossDomesticProductCAP))

#전처리된 numpy 생성
TIG_CoulumnExtract_np = TIG_CoulumnExtract.to_numpy()
MP_CoulumnExtract_np = MP_CoulumnExtract.to_numpy()
GDP_CoulumnExtract_np = GDP_CoulumnExtract.to_numpy()
PLI_CoulumnExtract_np = PLI_CoulumnExtract.to_numpy()
GDP_CoulumnExtractCAP_np = GDPCAP_CoulumnExtract.to_numpy()

# 전처리된 데이터에 존재하는 LOCATION 값 변수에 할당
P_TIG_Country = CountryExtractor(TIG_CoulumnExtract_np)[0]
P_MP_Contry = CountryExtractor(MP_CoulumnExtract_np)[0]
P_GDP_Country = CountryExtractor(GDP_CoulumnExtract_np)[0]
P_PLI_Country = CountryExtractor(PLI_CoulumnExtract_np)[0]
P_GDPCAP_Country = CountryExtractor(GDP_CoulumnExtractCAP_np)[0]

# csv 파일 업데이트
TIG_CoulumnExtract.to_csv("ProcessingDataset_Trust_in_government.csv",mode='w',index=False)
MP_CoulumnExtract.to_csv("ProcessingDataset_Multifactor_productivity.csv",mode='w',index=False)
GDP_CoulumnExtract.to_csv("ProcessingDataset_Gross_domestic_product.csv",mode='w',index=False)
PLI_CoulumnExtract.to_csv("ProcessingDataset_Price_level_indices.csv",mode='w',index=False)
GDPCAP_CoulumnExtract.to_csv("ProcessingDataset_Gross_domestic_productCAP.csv",mode='w',index=False)