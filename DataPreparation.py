#python version 3.9.12 64bit
import pandas as pd
def CountryExtractor(ListToExtract):# return(list of country, number of country included)
    ListOfCountry = []
    for i in range(len(ListToExtract)):
        if not(ListToExtract[i][0] in ListOfCountry):
            ListOfCountry.append(ListToExtract[i][0])
    return (ListOfCountry,len(ListOfCountry))
csv_TrustInGovernment = pd.read_csv("Dataset_Trust_in_government.csv")
csv_MultifactorProductivity = pd.read_csv("Dataset_Multifactor_productivity.csv")
csv_GrossDomesticProduct = pd.read_csv("Dataset_Gross_domestic_product_(GDP).csv")
csv_PriceLevelIndices = pd.read_csv("Dataset_Price_level_indices.csv")
#print(csv_TrustInGovernment)
#print(csv_MultifactorProductivity)
#print(csv_GrossDomesticProduct)
#print(csv_PriceLevelIndives)
csv_TrustInGovernment_np = csv_TrustInGovernment.to_numpy()
csv_MultifactorProductivity_np = csv_MultifactorProductivity.to_numpy()
csv_GrossDomesticProduct_np = csv_GrossDomesticProduct.to_numpy()
csv_PriceLevelIndices_np = csv_PriceLevelIndices.to_numpy()
print(CountryExtractor(csv_TrustInGovernment_np)[1])
print(CountryExtractor(csv_MultifactorProductivity_np)[1])
print(CountryExtractor(csv_GrossDomesticProduct_np)[1])
print(CountryExtractor(csv_PriceLevelIndices_np)[1])