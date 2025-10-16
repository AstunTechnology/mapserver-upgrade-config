# mapserver-upgrade-config

## Installation

Requires python 3+

Fetch latest egg file from dist directory and run (e.g.) `easy_install mapfile_utils-1.1.0-py2.7.egg`


## Development

* Clone the repo, change to the directory, create and activate a virtual environment.
* Install the repo as an editable package and install dependencies:
```sh
pip install -e .
pip install -r requirements
```

To run the tests use:

```sh
python -m unittest --failfast tests/test_map_to_xml.py
```
    
### Build a new release

* Update version number in `setup.py`
* Run `python setup.py bdist_wheel`
* Test by installing into another fresh virtual environment
* Add to repo via `git add --force dist/mapfile_utils-X.X.X-py3-none-any.whl`
  (replace `X.X.X` with the version number)
* Push to remote

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

# Notes
Any includes should be present in directory script is being run from. Can be empty files so touch will do.
