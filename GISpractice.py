import arcpy
import numpy as np

# Set the workspace environment
gdb = r".gdb"
arcpy.env.workspace = gdb

# List all feature classes within the "PYLON" feature dataset
feature_classes = arcpy.ListFeatureClasses(feature_dataset="PYLON")

# Define the fields to consider
fields = ["COMPOUND", "STRUCTURE", "FLOOR"]

# Create an empty list to store unique combinations
unique_combinations = []

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
        
        # Append the combinations to the unique_combinations list
        unique_combinations.extend(combinations.tolist())

# Print the unique combinations
for combination in unique_combinations:
    print(combination)