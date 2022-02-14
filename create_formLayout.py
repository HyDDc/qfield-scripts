import pandas as pd
import os
from qgis.PyQt.QtCore import QVariant
from qgis.core import *
from typing import  TypedDict
import json


#path = "/Users/huydoduc/Documents/DAI/blueprint_immobiliesKulturgut"
path = "/Users/huydoduc/Documents/DAI/blueprint_kgr2.json"

# load JSON - blueprint for KGR data model
with open(path) as f:
  data = json.load(f)

layers = QgsProject.instance().mapLayersByName('test')
if layers: 
    layer = layers[0]


l = layer 
prov = l.dataProvider()
fc = l.editFormConfig()
fc.clearTabs()
fc.setLayout(QgsEditFormConfig.TabLayout)
# Add fields

counter = 0

for i in range (len(data["Layout_Grundriss"])):
    #print(data["Layout2"][i])
    c = QgsAttributeEditorContainer(data["Layout_Grundriss"][i], fc.invisibleRootContainer())
    c.setIsGroupBox(False) # a tab
    
    for y in range(len(data["Layout"][i][data["Layout_Grundriss"][i]])):
        #print("innere Schleife")
        #print(data["Layout2"][i][data["Layout_Grundriss"][i]][y])
        c.addChildElement(QgsAttributeEditorField(data["Layout"][i][data["Layout_Grundriss"][i]][y], counter, c))

    fc.addTab(c)

# Add 1:N relations
#c_1_n = QgsAttributeEditorContainer("1:N links", fc.invisibleRootContainer())
#c_1_n.setIsGroupBox(False) # a tab
#fc.addTab(c_1_n)
#
#for rel in lyr['1_n']:
#    c_1_n.addChildElement(QgsAttributeEditorRelation(rel.name(), rel, c_1_n))

l.setEditFormConfig(fc)
