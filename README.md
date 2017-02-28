# mapserver-upgrade-config

##Installation
Requires python 2.7 

Requires `mappyfile` 

    pip install mappyfile
    
##Usage

    fix_mapfile [-o|--outputfile outputfile] [-t|-w int] inputfile
        WIDTH number of spaces to use in indenting XML
        -t use tabs not spaces
        
upgrade a mapfile to work with MapServer 5.4+ by adding VALIDATION blocks

    map_to_xml.py [-h] [-o OUTPUTFILE]  inputfile

converts a valid mapfile to XML

	xml_to_sld.py inputfile
	
convert a mapfile.xml to a dictionary of SLD elements indexed by layer name
