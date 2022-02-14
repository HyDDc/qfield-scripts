import pandas as pd
import os
from qgis.PyQt.QtCore import QVariant
from qgis.core import *
from typing import  TypedDict
import json

# set path for JSON
path = "/Users/huydoduc/Documents/DAI/blueprint_immobiliesKulturgut.json"
#path = "/Users/huydoduc/Documents/DAI/blueprint_kgr2.json"

# create Layer (Point, Line, Polygone)
layers = QgsProject.instance().mapLayersByName('test_immobiliesKG')


# load JSON - blueprint for KGR data model
with open(path) as f:
  data = json.load(f)

if layers: 
    layer = layers[0]

prov = layer.dataProvider()

field_names = [field.name() for field in prov.fields()]

caps = layer.dataProvider().capabilities()


all_features = data["ExternalResource"]+ data["TextEdit"]

print(all_features)


