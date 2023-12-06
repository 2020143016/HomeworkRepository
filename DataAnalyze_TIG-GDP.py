import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import math

# MergedData.csv 파일 읽어오기
CON_TIG_ALL = pd.read_csv("MergedData.csv")
# 그래프 생성
columnName1 = '(TIG)SND by TIME'
columnName2 = '(GDP)Change(%)'
x = CON_TIG_ALL[columnName1]
y = CON_TIG_ALL[columnName2]
dif,ax = plt.subplots()
ax.scatter(x,y)
ax.set_xlabel(columnName1)
ax.set_ylabel(columnName2)
plt.show()