#python version 3.9.12 64bit
import numpy as np
import pandas as pd
def CountryExtractor(ListToExtract):# return(list of country, number of country included)
    ListOfCountry = []
    for i in range(len(ListToExtract)):
        if not(ListToExtract[i][0] in ListOfCountry):
            ListOfCountry.append(ListToExtract[i][0])
    return (ListOfCountry,len(ListOfCountry))
def ExtractSameCountry(Target_list):# return list of country coexist in TrustInGovernment Data
    lst = []
    for i in CountryExtractor(csv_TrustInGovernment_np)[0]:
        if i in CountryExtractor(Target_list)[0]:
            lst.append(i)
    return lst
def DataProcessing(PandasData):# Delete not using columns
    lst = ['LOCATION','TIME','Value','Change of Value(%)']
    lstOfColumns = []
    for i in range(len(PandasData.columns)):
        if not(PandasData.columns[i] in lst):
            lstOfColumns.append(PandasData.columns[i])
    PDD = PandasData.drop(lstOfColumns,axis=1)
    return PDD
def EraseNotUsableData(PandasData):# Delete data with no use (location which doesn't exist in TIG, time not included in 2006~2022)
    idx = PandasData[~(PandasData['LOCATION'].isin(TIG_Country))|((PandasData['TIME'].astype('int')>2022) | (PandasData['TIME'].astype('int')<2006))].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
def EraseNotUsingDataForMP(PandasData):# delete AGRWTH
    idx = PandasData[PandasData['MEASURE'].astype('str') == 'AGRWTH'].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
def EraseNotUsingDataForGDP(PandasData):# delete USD_CAP
    idx = PandasData[PandasData['MEASURE'].astype('str') == 'USD_CAP'].index
    pdpd = PandasData.drop(idx,axis=0)
    return pdpd
csv_TrustInGovernment = pd.read_csv("Dataset_Trust_in_government.csv")
csv_MultifactorProductivity = pd.read_csv("Dataset_Multifactor_productivity.csv")
csv_GrossDomesticProduct = pd.read_csv("Dataset_Gross_domestic_product.csv")
csv_PriceLevelIndices = pd.read_csv("Dataset_Price_level_indices.csv")
csv_MultifactorProductivity = EraseNotUsingDataForMP(csv_MultifactorProductivity)
csv_GrossDomesticProduct = EraseNotUsingDataForGDP(csv_GrossDomesticProduct)
#print(csv_TrustInGovernment)
#print(csv_MultifactorProductivity)
#print(csv_GrossDomesticProduct)
#print(csv_PriceLevelIndives)

# adding amount of change column (become zero when current TIME minus 1 is not same to former TIME)
csv_GrossDomesticProduct['Data before available'] = np.where(csv_GrossDomesticProduct['TIME'].shift() == csv_GrossDomesticProduct['TIME']-1,1,0)
csv_MultifactorProductivity['Data before available'] = np.where(csv_MultifactorProductivity['TIME'].shift() == csv_MultifactorProductivity['TIME']-1,1,0)
csv_GrossDomesticProduct['Change of Value(%)'] = 100*csv_GrossDomesticProduct['Data before available']*(csv_GrossDomesticProduct['Value'] - csv_GrossDomesticProduct['Value'].shift(1))/csv_GrossDomesticProduct['Value'].shift(1)
csv_MultifactorProductivity['Change of Value(%)'] = 100*csv_MultifactorProductivity['Data before available']*(csv_MultifactorProductivity['Value'] - csv_MultifactorProductivity['Value'].shift(1))/csv_MultifactorProductivity['Value'].shift(1)

# pandas to numpy
csv_TrustInGovernment_np = csv_TrustInGovernment.to_numpy()
csv_MultifactorProductivity_np = csv_MultifactorProductivity.to_numpy()
csv_GrossDomesticProduct_np = csv_GrossDomesticProduct.to_numpy()
csv_PriceLevelIndices_np = csv_PriceLevelIndices.to_numpy()

# exsisting country
TIG_Country = CountryExtractor(csv_TrustInGovernment_np)[0]
MP_Contry = CountryExtractor(csv_MultifactorProductivity_np)[0]
GDP_Country = CountryExtractor(csv_GrossDomesticProduct_np)[0]
PLI_Country = CountryExtractor(csv_PriceLevelIndices_np)[0]

# Basic Data Processing
TIG_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_TrustInGovernment))
MP_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_MultifactorProductivity))
GDP_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_GrossDomesticProduct))
PLI_CoulumnExtract = DataProcessing(EraseNotUsableData(csv_PriceLevelIndices))

# processing data-pandas to numpy -------------------------------------
TIG_CoulumnExtract_np = TIG_CoulumnExtract.to_numpy()
MP_CoulumnExtract_np = MP_CoulumnExtract.to_numpy()
GDP_CoulumnExtract_np = GDP_CoulumnExtract.to_numpy()
PLI_CoulumnExtract_np = PLI_CoulumnExtract.to_numpy()

# processing data-exsisting country -------------------------------------
P_TIG_Country = CountryExtractor(TIG_CoulumnExtract_np)[0]
P_MP_Contry = CountryExtractor(MP_CoulumnExtract_np)[0]
P_GDP_Country = CountryExtractor(GDP_CoulumnExtract_np)[0]
P_PLI_Country = CountryExtractor(PLI_CoulumnExtract_np)[0]

#print processing data country existing(checking if it worked the way i intended)
# print(P_TIG_Country)
# print(P_MP_Contry)
# print(P_GDP_Country)
# print(P_PLI_Country)

# Basic Data Processing

#printing Basically Processed Data ------------------
print(TIG_CoulumnExtract)
print(MP_CoulumnExtract)
print(GDP_CoulumnExtract)
print(PLI_CoulumnExtract)

# csv data update -------------------------------------
TIG_CoulumnExtract.to_csv("ProcessingDataset_Trust_in_government.csv",mode='w',index=False)
MP_CoulumnExtract.to_csv("ProcessingDataset_Multifactor_productivity.csv",mode='w',index=False)
GDP_CoulumnExtract.to_csv("ProcessingDataset_Gross_domestic_product.csv",mode='w',index=False)
PLI_CoulumnExtract.to_csv("ProcessingDataset_Price_level_indices.csv",mode='w',index=False)