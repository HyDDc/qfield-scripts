import pandas as pd
from typing import  TypedDict

layers = QgsProject.instance().mapLayersByName('Schaden (Punkte)')
if layers: 
    layer = layers[0]

prov = layer.dataProvider()
#
field_names = [field.name() for field in prov.fields()]



for i in range (len(field_names)):
    ews = layer.editorWidgetSetup(i)  
    print(field_names[i])
    print("Type:", ews.type())
    print("Config:", ews.config())




#layer_csv = QgsVectorLayer(uri, 'Hilfe', 'delimitedtext')
#QgsProject.instance().addMapLayer(layer_csv)


#    
#uri = "file:///Users/huydoduc/Documents/DAI/Listen_QField/updated/Zustand.csv"    
#csv_file = pd.read_csv(uri, ";")
##csv_file = pd.read_csv(uri)
#
#
#print(csv_file.iloc[0])
#string = {}
#for i in range (len(csv_file)):
#    string[csv_file.iloc[i][0]]= csv_file.iloc[i][1]
#    #string = string + "{'"+csv_file.iloc[i][0]+"': '"+ csv_file.iloc[i][1]+"'},\n"
##string = string + "{'"+csv_file.iloc[len(csv_file)-1][0]+"': '"+ csv_file.iloc[len(csv_file)-1][1]+"'}"
#
#
#class Test(TypedDict):
#    code: str
#    beschreibung: str
#    
#class map(TypedDict):
#    map: dict
#    array: str
#
#map_alles = {}
#
##map: Test= { 'beschreibung':'y1'}
##map2: Test= {'code':'x2', 'beschreibung':'y2'}
##
#array_test = []
#
#for i in range (len(csv_file)):
#    map: Test= {csv_file.iloc[i][0]: csv_file.iloc[i][1]}
#    array_test.append(map)
#
#map_alles["map"]=array_test
##
#
#
#print(map_alles)
#    
##{'map': [{'Without need for action': 'UC-'},
##{'Long term from 3 years': 'UC0'},
##{'Intermediate term from 1 to 3 years': 'UC1'},
##{'Short term within 1 year': 'UC2'},
##{'Urgent and immediate within 3 month': 'UC3'}]}
#import json 
#
## load JSON - blueprint for KGR data model
#with open('/Users/huydoduc/Documents/DAI/blueprint_kgr2.json') as f:
#  data = json.load(f)
#
#
##print(data["Layout_Grundriss"])
#
#for i in range (len(data["Layout_Grundriss"])):
#    print(data["Layout2"][i])
#    for y in range(len(data["Layout2"][i][data["Layout_Grundriss"][i]])):
#        #print("innere Schleife")
#        #print(len(data["Layout2"][i][data["Layout_Grundriss"][i]]))
#        print(data["Layout2"][i][data["Layout_Grundriss"][i]][y])
#    
#    
    
    