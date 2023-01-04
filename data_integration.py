"""
Used to implement the data in the db database
"""
# Modules

import controller as ctrl

## DataFrame manipulation
import pandas as pd 

## Path
import glob as g

siren = ctrl.init_collection()

# Get the csv path
path = g.glob("./*.csv", recursive=True)[0]

# Upload the csv to the db
print("Uploading the csv to the database")
for i, chunk in enumerate(pd.read_csv(path, chunksize=1000000, low_memory=False)):
    x = siren.insert_many(chunk.to_dict(orient='records'))
    print("{}/34".format(i+1))

# Create an index based on the siren code 
print("Create an index based on the siret code ..")
siren.create_index("siret")