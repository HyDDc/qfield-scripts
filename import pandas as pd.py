import pandas as pd
import os
from qgis.PyQt.QtCore import QVariant
from qgis.core import *
from typing import  TypedDict
import json

# set path for JSON
path = "/Users/huydoduc/Documents/DAI/blueprint_immobiliesKulturgut"
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

for i in range (len(field_names)):
    if caps & QgsVectorDataProvider.DeleteAttributes: 
        res = layer.dataProvider().deleteAttributes([0])


def create_fields():
    caps = layer.dataProvider().capabilities()
    if caps & QgsVectorDataProvider.AddAttributes:
        for i in range (len(data["features"])):
            res = layer.dataProvider().addAttributes([QgsField((data["features"][i]), QVariant.String)])
            layer.updateFields()
    
    field_names = [field.name() for field in prov.fields()]
    for count, f in enumerate(field_names):
        print("{} {}".format(count, f))

    print("Fields wurden hinzugefügt")

create_fields()

def set_attachment():
    editor_widget_setup = QgsEditorWidgetSetup(
        'ExternalResource', 
        {
            'FileWidget': True,
            'DocumentViewer': 0,
            'RelativeStorage': 0,
            'StorageMode': 0,
            'DocumentViewerHeight': 0,
            'FileWidgetButton': True,
            'DocumentViewerWidth': 0,
            'FileWidgetFilter': ''
        })
        
    for i in range (len(data["ExternalResource"])):
        index = layer.fields().indexFromName(data["ExternalResource"][i])
        layer.setEditorWidgetSetup(index, editor_widget_setup)


set_attachment()

def setTextEdit():
    ## TextEdit: MultiLine: false 
    editor_widget_setup = QgsEditorWidgetSetup(
        'TextEdit', 
        {'IsMultiline': False, 'UseHtml': False}
        )
    for i in range (len(data["TextEdit"])):
        index = layer.fields().indexFromName(data["TextEdit"][i])
        layer.setEditorWidgetSetup(index, editor_widget_setup) 
        
    ## TextEdit2: MultiLine: true 
    editor_widget_setup = QgsEditorWidgetSetup(
        'TextEdit', 
        {'IsMultiline': True, 'UseHtml': False}
        )
    for i in range (len(data["TextEdit2"])):
        index = layer.fields().indexFromName(data["TextEdit2"][i])
        layer.setEditorWidgetSetup(index, editor_widget_setup) 
    

setTextEdit()

editor_widget_setup = QgsEditorWidgetSetup(
    'DateTime', 
    {'allow_null': True, 'calendar_popup': True,
    'display_format': 'yyyy-MM-dd', 'field_format': 'yyyy-MM-dd',
    'field_iso_format': False}
    )

index = layer.fields().indexFromName('datum')
layer.setFieldAlias(index, "Datum")
layer.setEditorWidgetSetup(index, editor_widget_setup)


# load all csv to set ValueRelation
# load by User interface

def setValueRelation():
    print("Checkboxen wurden eingestellt")
    
    for i in range (len(data["ValueRelation"])):
        field_val = data["ValueRelation"][i]
        #print(field_val)
        name = data["CSV"][i][data["ValueRelation"][i]][0]
        #print(name)
        csv_file = data["CSV"][i][data["ValueRelation"][i]][1]
        #print(csv_file)
        editor_widget_setup = QgsEditorWidgetSetup(
            'ValueRelation', 
            {'AllowMulti': True, 'AllowNull': False,
            'FilterExpression': '',
            'Key': name,
            'Layer': csv_file,
            'LayerName': csv_file,
            'LayerProviderName': 'ogr',
            #'LayerSource': '/Users/huydoduc/Downloads/Wansdorf_Schloss_neu_KGR1 2/1_Schaden_strukturell_2309.csv',
            'NofColumns': 1, 'OrderByValue': False,
            'UseCompleter': False,
            'Value': name
            })

        index = layer.fields().indexFromName(field_val)
        layer.setFieldAlias(index, name)
        layer.setEditorWidgetSetup(index, editor_widget_setup)

setValueRelation()

### ValueMap
def setValueMap():
    class Test(TypedDict):
        code: str
        beschreibung: str
        
    class map(TypedDict):
        map: dict
        array: str

    map_alles = {}
    array_test = []
    
    for y in range (len(data["ValueMap"])):
        
    
        project_path = QgsProject.instance().readPath("./")
        csv_path = "file://"+project_path+"/Listen/ValueMap/" + data["CSV_ValueMap"][y]+".csv"

        #uri = "file:///Users/huydoduc/Documents/DAI/Listen_QField/updated/Significance.csv"    
        uri = csv_path
        csv_file = pd.read_csv(uri, ";")

        for i in range (len(csv_file)):
            map: Test= {csv_file.iloc[i][1]: csv_file.iloc[i][0]}
            array_test.append(map)

        map_alles["map"]=array_test

        editor_widget_setup = QgsEditorWidgetSetup('ValueMap', map_alles)

        index = layer.fields().indexFromName(data["ValueMap"][y])
        layer.setFieldAlias(index, data["CSV_ValueMap"][y])
        layer.setEditorWidgetSetup(index, editor_widget_setup)


setValueMap()



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


