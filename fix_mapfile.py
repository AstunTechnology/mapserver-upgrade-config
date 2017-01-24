# open the MapFile
class fix_mapfile:
    """A class to fix mapfiles while moving from 6.0 to 6.4.
    
    See UTILS-328 for full discussion, basically move validation patterns from METADATA to VALIDATION
    blocks.
    
     
    
    :param filename: the name of the map file to fix
    :param width: number of spaces per indent level if using spaces (default 2)
    :param tabs: boolean should output be indented with tabs or spaces (default false)  
    
    """
    def __init__(self,filename, width=2, tabs = False):
        self.filename = filename
        self.width = width
        self.tabs = tabs
        self.openings = ['class','validation','map','layer','outputformat', 'metadata','legend','label','querylayer','scalebar','web','style','querymap',
                'projection']
        
        

    def generate_indent(self, indent):
        if self.tabs:
            start = '\t' * indent
        else:
            start = ' ' * (indent * self.width)
        return start

    
    def fix(self):
        """prints the fixed file to std out
    
        """
        in_meta = False
        indent = 0;
        pattern_line = ""
        with open(self.filename) as fp:
            for line in fp:
                sline = line.strip().lower()
                if sline in self.openings:              
                    
                    if('metadata' in sline):
                        in_meta = True
                        lines = []
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
                            print self.generate_indent(indent)+pattern_line
                            indent -= 1
                            print self.generate_indent(indent)+"END"
                        line = '' # dispose of spare END
                        pattern_line=''
                        
                if 'validation_pattern' in sline:
                    bits=sline.split('_')
                    pattern = bits[-1].split()[-1]
                    pattern_line = bits[0]+'" '+pattern
                    line='' # delete the line from the input
                        
                if (line.rstrip() != '' and not in_meta):
                    print self.generate_indent(indent) + line.strip();
                    
                if(line.rstrip() != '' and in_meta):
                    lines.append(line.strip())

