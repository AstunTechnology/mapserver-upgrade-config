#!/usr/bin/python

import sys
import shutil

# open the MapFile
class fix_mapfile:
    """A class to fix mapfiles while moving from 6.0 to 6.4.
    
    See UTILS-328 for full discussion, basically move validation patterns from METADATA to VALIDATION
    blocks.
    
     
    
    :param input: the name of the map file to fix
    :param width: number of spaces per indent level if using spaces (default 2)
    :param tabs: boolean should output be indented with tabs or spaces (default false)  
    
    """
    def __init__(self,input_file, output_file="", width=2, tabs = False):
        self.input = input_file
        self.output = output_file
        self.width = width
        self.tabs = tabs
        if self.output:
            sys.stdout = open(self.output,'w')
            
        self.openings = ['class','validation','map','layer','outputformat', 'metadata','legend','label','querylayer','scalebar','web','style','querymap',
                'projection','symbol']
        
        

    def generate_indent(self, indent):
        if self.tabs:
            start = '\t' * indent
        else:
            start = ' ' * (indent * self.width)
        return start

    
    def fix(self):
        """prints the fixed file to std out or output file
    
        """
        in_meta = False
        indent = 0;
        pattern_line = ""
        with open(self.input) as fp:
            for line in fp:
                sline = line.strip().lower()
                if sline in self.openings:              
                    
                    if('metadata' in sline):
                        in_meta = True
                        lines = []
                        pattern_line = []
                    else:
                        print self.generate_indent(indent) + line.strip();
                    indent+=1
                    line='' 
                        
                
                if(sline == 'end'):
                    indent-=1   
                    if(in_meta):
                        in_meta = False
                        if len(lines) > 0:
                            print self.generate_indent(indent)+"METADATA"
                            for l in lines:
                                print self.generate_indent(indent+1)+l
                            print self.generate_indent(indent)+"END"
                        if pattern_line:
                            print self.generate_indent(indent)+"VALIDATION"
                            indent += 1
                            for p in pattern_line:
                                print self.generate_indent(indent)+p
                            indent -= 1
                            print self.generate_indent(indent)+"END"
                        line = '' # dispose of spare END
                        pattern_line=[]
                        
                if 'validation_pattern' in sline:
                    bits=sline.split('_')
                    pattern = bits[-1].split()[-1]
                    pattern_line.append(bits[0]+'" '+pattern)
                    line='' # delete the line from the input
                        
                if (line.rstrip() != '' and not in_meta):
                    print self.generate_indent(indent) + line.strip();
                    
                if(line.rstrip() != '' and in_meta):
                    lines.append(line.strip())


def main():
    for arg in sys.argv[1:]:
        #copy to backup and run fix
        shutil.copy(arg, arg+".bak")
        fixer = fix_mapfile(arg+".bak",arg)
        fixer.fix()
     

if __name__ == "__main__":
    main()        