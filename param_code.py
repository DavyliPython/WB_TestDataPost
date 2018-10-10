import pandas as pd

paramFile=r'C:\onedrive\OneDrive - Honeywell\VPD\parameters code.csv'
columName = ['param', 'paramDesc', 'paramDescChs','unit','unitM','unitChs','rate']
paramDF = pd.read_csv(paramFile, names = columName, index_col = 0,  header = 0 )

print(list(paramDF.index))
print(list (paramDF['paramDesc']))

#x = paramDF.loc['ABCVIINR','paramDescChs']

def getParamInfo(param, colName):
    #x = paramDF.loc[param, columName]
    return (paramDF.loc[param, colName] )


print(getParamInfo('ABCVIINR','paramDesc'))
print(getParamInfo('ABCVIINR','paramDescChs'))
print(getParamInfo('ABCVIINR','unit'))

print(getParamInfo('BRKMLO2','paramDesc'))
print(getParamInfo('BRKMLO2','paramDescChs'))
print(getParamInfo('BRKMLO2','unit'))