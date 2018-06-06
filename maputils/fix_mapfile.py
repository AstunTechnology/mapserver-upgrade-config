#!/usr/bin/python
from __future__ import print_function
import argparse
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# open the MapFile
class fix_mapfile:
    """A class to fix mapfiles while moving from 6.0 to 6.4.
    
    See UTILS-328 for full discussion, basically move validation patterns from METADATA to VALIDATION
    blocks.
    
     
    
    :param input: the name of the map file to fix
    :param width: number of spaces per indent level if using spaces (default 2)
    :param tabs: boolean should output be indented with tabs or spaces (default false)  
    
    """
    def __init__(self, input_file, output_file="", width=2, tabs=False):
        self.input = input_file
        self.output = output_file
        self.width = width
        self.tabs = tabs
        if self.output:
            sys.stdout = open(self.output, 'w')
            
        self.openings = ['class', 'validation', 'map', 'layer', 'outputformat', 'metadata', 'legend', 'label', 'querylayer', 'scalebar', 'web', 'style', 'querymap',
                'projection']
        
        

    def generate_indent(self, indent):
        if self.tabs:
            start = '\t' * indent
        else:
            start = ' ' * (indent * self.width)
        return start

    
    def fix(self):
        """prints the fixed file to std out or output file
    
        """
        in_layer = False
        any_meta = False
        in_meta = False
        indent = 0;
        in_count = 0;
        pattern_line = ""
        with open(self.input) as fp:
            for line in fp:
                sline = line.strip().lower()
                if sline in self.openings:              
                    if('layer' in sline):
                        in_layer = True
                        any_meta = False
                        in_count = 0
                    if('metadata' in sline):
                        in_meta = True
                        any_meta = True
                        lines = []
                        pattern_line = []
                    else:
                        print (self.generate_indent(indent) + line.strip())
                    indent += 1
                    in_count+= 1
                    line = '' 
                        
                
                if(sline == 'end'): 
                    indent -= 1   
                    if(in_meta):
                        in_meta = False
                        if len(lines) > 0:
                            print ( self.generate_indent(indent) + "METADATA")
                            for l in lines:
                                print ( self.generate_indent(indent + 1) + l)
                            print ( self.generate_indent(indent) + "END")
                        if pattern_line:
                            print ( self.generate_indent(indent) + "VALIDATION")
                            indent += 1
                            for p in pattern_line:
                                print ( self.generate_indent(indent) + p)
                            indent -= 1
                            print ( self.generate_indent(indent) + "END")
                        elif in_layer:
                            print ( self.generate_indent(indent) + "VALIDATION")
                            indent += 1
                            print ( self.generate_indent(indent) + '"qstring" "."')
                            indent -= 1
                            print ( self.generate_indent(indent) + "END")
                        line = ''  # dispose of spare END
                        pattern_line = []
                    if in_layer and in_count == 0 and not any_meta:
                        print ( self.generate_indent(indent) + "VALIDATION")
                        indent += 1
                        print ( self.generate_indent(indent) +
                        '"qstring_validation_pattern" "."')
                        indent -= 1
                        print ( self.generate_indent(indent) + "END")
                    in_count-=1
                    
                if 'validation_pattern' in sline:
                    bits = sline.split('_')
                    pattern = bits[-1].split()[-1]
                    start=''
                    if not bits[0].startswith('"'):
                        start='"'
                    pattern_line.append(start+bits[0] + '" ' + pattern)
                    line = ''  # delete the line from the input
                        
                if (line.rstrip() != '' and not in_meta):
                    #eprint("printing",line.strip())
                    if('symbol' in sline):
                        parts = line.split()
                        oline = self.generate_indent(indent) + parts[0]
                        for p in parts[1:]:
                            if not '"' in p and not "'" in p:
                                oline+=' "'+p+'"'
                            else:
                                oline += ' '+p
                        print(oline)
                    else:
                        print (self.generate_indent(indent) + line.strip())
                    
                if(line.rstrip() != '' and in_meta):
                    lines.append(line.strip())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile", type=str, help="the map file to be processed")
    parser.add_argument("-o", "--outputfile", type=str, help="the file to write output to (stdout if missing)", default="")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--tabs", help="use tabs instead of spaces", action="store_true", default=False)
    group.add_argument("-w", "--width", help="number of spaces for indentation", default=2, type=int)
    
    args = parser.parse_args()
    
    use_tabs = False
    if args.tabs:
        use_tabs = True
        print ( use_tabs)
    # copy to backup and run fix
    # shutil.copy(infile, backup)
    fixer = fix_mapfile(args.inputfile, tabs=use_tabs, output_file=args.outputfile, width=args.width)
    fixer.fix()
     

if __name__ == "__main__":
    main()        
