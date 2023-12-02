#python version 3.9.12 64bit
from ast import Delete
from statistics import mode
import pandas as pd
import os
def CountryExtractor(ListToExtract):# return(list of country, number of country included)
    ListOfCountry = []
    for i in range(len(ListToExtract)):
        if not(ListToExtract[i][0] in ListOfCountry):
            ListOfCountry.append(ListToExtract[i][0])
    return (ListOfCountry,len(ListOfCountry))
def ExtractSameCountry(Target_list):
    lst = []
    for i in CountryExtractor(csv_TrustInGovernment_np)[0]:
        if i in CountryExtractor(Target_list)[0]:
            lst.append(i)
    return lst
def DataProcessing(PandasData):
    lst = ['LOCATION','TIME','Value']
    lstOfColumns = []
    for i in range(len(PandasData.columns)):
        if not(PandasData.columns[i] in lst):
            lstOfColumns.append(PandasData.columns[i])
    PDD = PandasData.drop(lstOfColumns,axis=1)
    return PDD
csv_TrustInGovernment = pd.read_csv("Dataset_Trust_in_government.csv")
csv_MultifactorProductivity = pd.read_csv("Dataset_Multifactor_productivity.csv")
csv_GrossDomesticProduct = pd.read_csv("Dataset_Gross_domestic_product.csv")
csv_PriceLevelIndices = pd.read_csv("Dataset_Price_level_indices.csv")
#print(csv_TrustInGovernment)
#print(csv_MultifactorProductivity)
#print(csv_GrossDomesticProduct)
#print(csv_PriceLevelIndives)

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

#print(csv_TrustInGovernment)
#print(csv_MultifactorProductivity)
#print(csv_GrossDomesticProduct)
#print(csv_PriceLevelIndices)

#delete column except time,location, value
TIG_CoulumnExtract = DataProcessing(csv_TrustInGovernment)
MP_CoulumnExtract = DataProcessing(csv_MultifactorProductivity)
GDP_CoulumnExtract = DataProcessing(csv_GrossDomesticProduct)
PLI_CoulumnExtract = DataProcessing(csv_PriceLevelIndices)

print(TIG_CoulumnExtract)
print(MP_CoulumnExtract)
print(GDP_CoulumnExtract)
print(PLI_CoulumnExtract)
TIG_CoulumnExtract.to_csv("ProcessingDataset_Trust_in_government.csv",mode='w',index=False)
MP_CoulumnExtract.to_csv("ProcessingDataset_Multifactor_productivity.csv",mode='w',index=False)
GDP_CoulumnExtract.to_csv("ProcessingDataset_Gross_domestic_product.csv",mode='w',index=False)
PLI_CoulumnExtract.to_csv("ProcessingDataset_Price_level_indices.csv",mode='w',index=False)