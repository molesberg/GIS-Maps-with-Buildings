import arcpy
import numpy as np

# Set the workspace environment
gdb = r"D:\ArcGIS Pro\Projects\Unclass build\Localtest.gdb"
arcpy.env.workspace = gdb

# List all feature classes within the "PYLON" feature dataset
feature_classes = arcpy.ListFeatureClasses(feature_dataset="Portaldataoffline")

def getcombos():
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

combos = getcombos()
# Print the unique combinations
for combination in combos:
    print(combination)

#list of unique compounds
comp = np.unique(combos[:, 0])
print('\n', comp)