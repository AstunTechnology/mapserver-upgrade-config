'''
Created on 28 Jun 2017

@author: ian
'''
import sys
import mappyfile
import json
mapfile = open( sys.argv[1], "r" )
mf = mappyfile.load( mapfile )

if len(sys.argv)==3:
    sys.stdout = open(sys.argv[2], 'w')

json.dump(mf, sys.stdout, indent=4)
