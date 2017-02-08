'''
Created on 30 Jan 2017

@author: ian
'''

import argparse
import sys
 

import mappyfile

# import dicttoxml
# from xml.dom.minidom import parseString
from lxml import etree
import plyplus
from xml.sax.saxutils import escape
from operator import attrgetter
import operator

class map_to_xml(object):
    """
    
    :param input: the name of the map file to fix
    :param width: number of spaces per indent level if using spaces (default 2)
    :param tabs: boolean should output be indented with tabs or spaces (default false)  
    
    """
    keyCases = {"anchorpoint":"anchorPoint",
"backgroundcolor":"backgroundColor",
"browseformat":"browseFormat",
"classgroup":"classGroup",
"classitem":"classItem",
"colorattribute":"colorAttribute",
"connectiontype":"connectionType",
"datapattern":"dataPattern",
"defresolution":"defResolution",
"filteritem":"filterItem",
"fontset":"fontSet",
"formatoption":"formatOption",
"geomtransform":"geomTransform",
"imagecolor":"imageColor",
"imagemode":"imageMode",
"imagepath":"imagePath",
"imagetype":"imageType",
"imageurl":"imageUrl",
"initialgap":"initialGap",
"keyimage":"keyImage",
"keysize":"keySize",
"keyspacing":"keySpacing",
"labelcache":"labelCache",
"labelformat":"labelFormat",
"labelitem":"labelItem",
"labelleader":"LabelLeader",
"labelmaxscaledenom":"labelMaxScaleDenom",
"labelminscaledenom":"labelMinScaleDenom",
"labelrequires":"labelRequires",
"legendformat":"legendFormat",
"linecap":"lineCap",
"linejoin":"lineJoin",
"linejoinmaxsize":"lineJoinMaxSize",
"markersize":"markerSize",
"maxarcs":"maxArcs",
"maxboxsize":"maxBoxSize",
"maxfeatures":"maxFeatures",
"maxgeowidth":"maxGeoWidth",
"maxinterval":"maxInterval",
"maxlength":"maxLength",
"maxoverlapangle":"maxOverlapAngle",
"maxscaledenom":"maxScaleDenom",
"maxsize":"maxSize",
"maxsubdivide":"maxSubdivide",
"maxtemplate":"maxTemplate",
"maxwidth":"maxWidth",
"mimetype":"mimeType",
"minarcs":"minArcs",
"minboxsize":"minBoxSize",
"mindistance":"minDistance",
"minfeaturesize":"minFeatureSize",
"mingeowidth":"minGeoWidth",
"mininterval":"minInterval",
"minscaledenom":"minScaleDenom",
"minsize":"minSize",
"minsubdivide":"minSubdivide",
"mintemplate":"minTemplate",
"minwidth":"minWidth",
"outlinecolor":"outlineColor",
"outlinecolorattribute":"outlineColorAttribute",
"outlinewidth":"outlineWidth",
"outputformat":"OutputFormat",
"polaroffset":"polarOffset",
"postlabelcache":"postLabelCache",
"queryformat":"queryFormat",
"querymap":"QueryMap",
"repeatdistance":"repeatDistance",
"scaledenom":"scaleDenom",
"shadowcolor":"shadowColor",
"shadowsize":"shadowSize",
"shapepath":"shapePath",
"sizeunits":"sizeUnits",
"styleitem":"styleItem",
"symbolscaledenom":"symbolScaleDenom",
"symbolset":"symbolSet",
"templatepattern":"templatePattern",
"temppath":"tempPath",
"tileindex":"tileIndex",
"tileitem":"tileItem",
"toleranceunits":"toleranceUnits",
"patterns":"pattern",
"metadata":"Metadata"
}
    def makeSubElement(self, root, elements, key, upper=False):
        if "__type__" == key:
            return None
        if key in self.keyCases:
            keyx = self.keyCases[key]
        else:
            keyx = key
        el = etree.SubElement(root, keyx)
        
        element = elements[key]
        if isinstance(element, plyplus.common.TokValue):  
            el.text = escape(element).replace("'", "").replace("\"", "")
        elif key.find("color") > -1:
            el.set("red", str(element[0]))
            el.set("green", str(element[1]))
            el.set("blue", str(element[2]))
        elif (key.find("size") > -1 or key == 'keyspacing' or key == 'offset') and isinstance(element, list):
            el.set("x",str(element[0]))
            el.set("y",str(element[1]))
        elif isinstance(element, list):
            if any(isinstance(el, list) for el in element):
                # lis = list(itertools.chain.from_iterable(element))
                lis = reduce(operator.add, element)
                #lis = reduce(operator.add, lis)
                el.text = " ".join(str(i) for i in lis)
            else: 
                el.text = " ".join(str(i) for i in element)
        else:
            el.text = str(element).replace("'", "").replace("\"", "")
        if upper:
            el.text = el.text.upper()
        return el


    def makeLegend(self, root, mapp, mapkey):
        legend = etree.SubElement(root, "Legend")
        for leg in mapp[mapkey]:
            for k in leg.keys():
                if "labels" == k:
                    self.makeLabels(leg, legend, k)
                elif 'status' == k:
                    legend.set("status",leg[k].upper())
                else:  
                    self.makeSubElement(legend, leg, k)
        legend = self.sortChildren(legend, legend)
        


    def makeLabels(self, s, class_, k):
        for kx in s[k]:
            labels = etree.SubElement(class_, "Label")
            for ky in kx:
                if 'type' == ky:
                    labels.set("type", kx[ky].upper())
                elif 'position' == ky:
                    self.makeSubElement(labels, kx, ky, upper=True)
                else:
                    self.makeSubElement(labels, kx, ky)
            
            labels = self.sortChildren(labels, labels)
        
        return kx

    def makeLayers(self, root, mapp, mapkey):
        for l in mapp[mapkey]:    
            layer = etree.SubElement(root, "Layer", name=l["name"].replace("\"", ""))
            for key in l.keys():
                if "include" == key:
                # import the file?
                    pass
                elif "name" == key:
                    pass
                elif "status" == key:
                    layer.set("status", l[key])
                elif "type" == key:
                    layer.set("type", l[key])
                elif "classes" == key:
                    
                    for s in l[key]:
                        class_ = etree.SubElement(layer, "Class")
                        for k in s.keys():
                            if k == 'name' or k == 'status':
                                class_.set(k, s[k].replace('"', '').replace("'", ""))
                            elif k == 'styles':
                                st = s['styles']
                                
                                for sty in st:
                                    stEl = etree.SubElement(class_, "Style")
                                    for key in sty.keys():
                                        self.makeSubElement(stEl, sty, key)
                                    stEl = self.sortChildren(stEl, stEl)
                            elif "labels" == k:
                                kx = self.makeLabels(s, class_, k)
                            else:
                                self.makeSubElement(class_, s, k)           
                        class_ = self.sortChildren(class_, class_)        
                
                elif "metadatas" == key:
                    meta = etree.SubElement(layer, "Metadata")
                    c = l["metadatas"]
                    
                    for kx in c:
                        for k in kx:
                            if k == '__type__':
                                pass
                            else:
                                item = etree.SubElement(meta, "item", name=l[k][0].replace("'", "").replace("\"", ""))
                                item.text = l[k][1].replace("'", "").replace("\"", "")
                elif "validation" == key:
                    validation = etree.SubElement(layer, "Validation")
                    for k in l["validation"]:
                        item = etree.SubElement(validation, "item", name=k[0].replace("'", "").replace("\"", ""))
                        item.text = k[1].replace("'", "").replace("\"", "")
                    
                else:
                    self.makeSubElement(layer, l, key)
            layer = self.sortChildren(layer, layer)
            
    def makeQueryMaps(self, root, mapp, mapkey):
        qmap = etree.SubElement(root, "QueryMap")
        for leg in mapp[mapkey]:
            for k in leg.keys():
                if 'status' == k:
                    qmap.set(k,leg[k])
                else:
                    self.makeSubElement(qmap, leg, k)
    
    
    def makeWebs(self, root, mapp, mapkey):
        webs = etree.SubElement(root, "Web")
        for k in mapp[mapkey]:
            if "metadata" == k:
                meta = etree.SubElement(webs, "Metadata")
                c = mapp[mapkey]["metadata"]
                for kx in c:
                    item = etree.SubElement(meta, "item", name=kx.replace("'", "").replace("\"", ""))
                    item.text = c[kx].replace("'", "").replace("\"", "")
                        
            else:
                self.makeSubElement(webs, mapp[mapkey], k)
        webs = self.sortChildren(webs, webs)
    
    def makeOutputFormats(self, root, mapp, mapkey):
        # outputformats = etree.SubElement(root, mapkey)
        for fmt in mapp[mapkey]:
            outputformat = etree.SubElement(root, "OutputFormat")
            for k in fmt.keys():
                if 'name' == k:
                    outputformat.set(k,fmt[k])
                else:
                    self.makeSubElement(outputformat, fmt, k)
            outputformat = self.sortChildren(outputformat, outputformat)
        
    def makeProjections(self, root, mapp, mapkey):
        #proj = etree.SubElement(root, "Projections")
        for k in mapp[mapkey]:
                el = etree.SubElement(root, "projection")
                el.text = str(" ".join(k)).replace("'", "").replace("\"", "")
    

    def makeScalebars(self, root, mapp, mapkey):
        scalebars = etree.SubElement(root, "ScaleBar");
        for leg in mapp[mapkey]:
            for k in leg.keys():
                if 'labels' == k:
                    self.makeLabels(leg, scalebars, k)
                elif 'status' == k:
                    scalebars.set(k,leg[k])
                else:
                    self.makeSubElement(scalebars, leg, k)
        scalebars = self.sortChildren(scalebars, scalebars)
    
    def makeConfig(self, root, mapp, mapkey):
        # this currently doesn't find any but the last config - needs a mod in mappyfile!
        
        el = etree.SubElement(root, "Config")
        for k in mapp[mapkey].keys():
            item = etree.SubElement(el, "item", name=k[0])
            item.text = k[1]
    

    def sortChildren(self, root, new_root):
        temp = sorted(set(root), key=lambda x:attrgetter('tag')(x).lower())
        for x in temp:
            new_root.append(x)
        
        return new_root

    def __init__(self, input_file, output_file="", width=2, tabs=False):
        self.input = input_file
        self.output = output_file
        self.width = width
        self.tabs = tabs
        if self.output:
            sys.stdout = open(self.output, 'w')
            
        #parser = mappyfile.parser.Parser()
        root = etree.Element("Map", nsmap={None:"http://www.mapserver.org/mapserver"},
                             name=input_file, version="5.6")
        #map_ = parser.parse_file(input_file)
    
        
        mapp = mappyfile.utils.load(input_file)
        for mapkey in mapp.keys():
            if "include" == mapkey:
                # import the file?
                pass
            elif "legends" == mapkey:
                self.makeLegend(root, mapp, mapkey)
            elif mapkey == 'layers':
                self.makeLayers(root, mapp, mapkey)
            elif mapkey == 'querymaps':
                self.makeQueryMaps(root, mapp, mapkey)
            elif mapkey == 'web':
                self.makeWebs(root, mapp, mapkey)
            elif mapkey == 'outputformats':
                self.makeOutputFormats(root, mapp, mapkey)
            elif mapkey == 'projections':
                self.makeProjections(root, mapp, mapkey)
            elif mapkey == 'scalebars':
                self.makeScalebars(root, mapp, mapkey)
            elif mapkey == 'config':
                self.makeConfig(root, mapp, mapkey)
            elif 'name' == mapkey:
                root.set("name",mapp['name'])
            elif 'status' == mapkey:
                root.set("status",mapp['status'].upper())
            else: 
                self.makeSubElement(root, mapp, mapkey)              
                
        # sort tag order to comply with XSD
        root = self.sortChildren(root, etree.Element("Map", nsmap={None:"http://www.mapserver.org/mapserver"},
                             name=input_file, version="5.6"))
                             
        print(etree.tostring(root, pretty_print=True))
        self.map_root = root
       
            
        
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
        print use_tabs
    # copy to backup and run fix
    # shutil.copy(infile, backup)
    mapper = map_to_xml(args.inputfile, tabs=use_tabs, output_file=args.outputfile, width=args.width)
    
    # for el in mapper.map_root:
        # print el
     

if __name__ == "__main__":
    main()        