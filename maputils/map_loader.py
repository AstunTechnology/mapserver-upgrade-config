'''
Created on 28 Jun 2017

@author: ian
'''
import mappyfile
import json
mapfile = open( "/home/ian/Downloads/MVDC_layers_MyMapsEveryone.map", "r" )
mf = mappyfile.load( mapfile )

with open("./docs/examples/sample.json", "w") as f:
    json.dump(mf, f, indent=4)
