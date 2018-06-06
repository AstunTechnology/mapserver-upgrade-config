'''
Created on 28 Jun 2017

@author: ian
'''
import sys
import argparse
import mappyfile
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "mapfile" )
    args = parser.parse_args()
    mapfile = open( args.mapfile, "r" )
    mf = mappyfile.load( mapfile)

    if len(sys.argv)==3:
        sys.stdout = open(sys.argv[2], 'w')

    json.dump(mf, sys.stdout, indent=4)

if __name__ == "__main__":
    main()        

