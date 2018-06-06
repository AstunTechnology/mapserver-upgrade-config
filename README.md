# mapserver-upgrade-config

## Installation

Requires python 2.7 


    
## Usage

    fix-map [-o|--outputfile outputfile] [-t|-w int] inputfile
        WIDTH number of spaces to use in indenting XML
        -t use tabs not spaces
        
upgrade a mapfile to work with MapServer 6.4+ by adding VALIDATION blocks.

    map-to-xml [-h] [-o OUTPUTFILE]  inputfile

converts a valid mapfile to XML.

	xml-to-sld inputfile
	
convert a mapfile.xml to a dictionary of SLD elements indexed by layer name.

    load-map file.map
    
converts a mapfile to JSON, really only useful as a test of correctness.
