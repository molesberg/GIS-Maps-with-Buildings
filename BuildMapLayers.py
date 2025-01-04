import arcpy
import numpy as np
import time

# Set the workspace environment
gdb = r"D:\ArcGIS Pro\Projects\Unclass build\Localtest.gdb"
aprxpath = r"D:\ArcGIS Pro\Projects\Unclass build\Unclass build.aprx"
mapname = "Lorien SecondAge"
arcpy.env.workspace = gdb
aprx = arcpy.mp.ArcGISProject(aprxpath)
map = aprx.listMaps(mapname)[0]

def getcombos(fds):
    feature_classes = arcpy.ListFeatureClasses(feature_dataset=fds)
    # Define the fields to consider
    fields = ["COMPOUND", "STRUCTURE", "FLOOR"]

    # Create an empty list to store unique combinations
    combos = []

    # Loop through each feature class
    for fc in feature_classes:
        # Get the field names present in the feature class
        field_names = [field.name for field in arcpy.ListFields(fc)]
        
        # Check if all the fields are present in the feature class
        if all(field in field_names for field in fields):
            # Retrieve the field values using a numpy array
            values = arcpy.da.TableToNumPyArray(fc, fields)
            
            # Find unique combinations of the fields using numpy.unique
            combinations = np.unique(values)
            
            # Append the combinations to the combos list
            combos.extend(combinations.tolist())

    # M: Isolate overlap between features
    combos =  np.unique(combos, axis = 0)
    return combos

combos = getcombos("Portaldataoffline")

#list of unique compounds
comps = np.unique(combos[:, 0])

layers = map.listLayers()
for i, lyr in enumerate(layers):
    if lyr.name == "Campus Template":
        g = i
    elif lyr.name == "Building Template":
        b = i
    elif lyr.name == "Floor Template":
        t = i
    elif lyr.name == "Roof Template":
        r = i
groupl = layers[g]
buildingl = layers[b]
floorl = layers[t]
roofl = layers[r]

for lyr in map.listLayers():
    if lyr.name == "Interior" and lyr.isGroupLayer:
        for comp in comps:
            groupl.name = comp
            map.addLayerToGroup(lyr, groupl, "BOTTOM")
groupl.name = "Campus Template" #I haven't figured out how to create a copy without changing the name of the target layers, so this resets the existing layer

#I built the below before realizing adding a group layer would copy all layers under it. Need to adjust acknowledging there's data under
#Easiest solution will to build a copy template which has structure, building, and floor groups separate. May be wise to have a roof group layer also

for lyr in map.listLayers(): #map template layers will need to be changed to be called "template". Group layers bring all sublayers with them
    if "EXTERIOR" in lyr.longName.upper():
        continue
    elif lyr.isGroupLayer:
        if lyr.name in comps:
            mask = np.isin(combos[:,0], lyr.name)
            stru = combos[:,1][mask]
            stru = np.unique(stru)
            for st in stru:
                buildingl.name = st
                map.addLayerToGroup(lyr, buildingl, "BOTTOM")
buildingl.name = "Building Template" 

for lyr in map.listLayers(): #map template layers will need to be changed to be called "template"
    if "EXTERIOR" in lyr.longName.upper():
        continue 
    elif lyr.isGroupLayer:
        for combo in combos:
            if combo[0] in lyr.longName and combo[1] in lyr.name:
                if "ROOF" in combo[2].upper():
                    roofl.name = combo[2]
                    map.addLayerToGroup(lyr, roofl, "BOTTOM")
                else:
                    floorl.name = combo[2]
                    map.addLayerToGroup(lyr, floorl, "BOTTOM")
floorl.name = "Floor Template" 
roofl.name = "Roof Template" 

#next need to build definition queries for feature layers

#then set data sources to target gdb

#then delete any feature layers which are empty

aprx.save()
print("Exit ", time.ctime())
