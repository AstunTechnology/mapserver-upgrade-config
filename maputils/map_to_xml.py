'''
Created on 30 Jan 2017

@author: ian
'''
import argparse
import sys
import io
import re
import mappyfile
from functools import reduce  # python 3
# import dicttoxml
# from xml.dom.minidom import parseString
from lxml import etree
from lxml.etree import CDATA

# import plyplus
# from xml.sax.saxutils import escape
from operator import attrgetter
import operator
import logging


class map_to_xml(object):
    """
    :param input: the name of the map file to fix
    :param width: number of spaces per indent level if using spaces (default 2)
    :param tabs: boolean should output be indented with tabs or spaces
       (default false)
    """
    keyCases = {"anchorpoint": "anchorPoint",
                "backgroundcolor": "backgroundColor",
                "browseformat": "browseFormat",
                "classgroup": "classGroup",
                "classitem": "classItem",
                "colorattribute": "colorAttribute",
                "connectiontype": "connectionType",
                "datapattern": "dataPattern",
                "defresolution": "defResolution",
                "filteritem": "filterItem",
                "fontset": "fontSet",
                "formatoption": "formatOption",
                "geomtransform": "geomTransform",
                "imagecolor": "imageColor",
                "imagemode": "imageMode",
                "imagepath": "imagePath",
                "imagetype": "imageType",
                "imageurl": "imageUrl",
                "initialgap": "initialGap",
                "keyimage": "keyImage",
                "keysize": "keySize",
                "keyspacing": "keySpacing",
                "labelcache": "labelCache",
                "labelformat": "labelFormat",
                "labelitem": "labelItem",
                "labelleader": "LabelLeader",
                "labelmaxscaledenom": "labelMaxScaleDenom",
                "labelminscaledenom": "labelMinScaleDenom",
                "labelrequires": "labelRequires",
                "legendformat": "legendFormat",
                "linecap": "lineCap",
                "linejoin": "lineJoin",
                "linejoinmaxsize": "lineJoinMaxSize",
                "markersize": "markerSize",
                "maxarcs": "maxArcs",
                "maxboxsize": "maxBoxSize",
                "maxfeatures": "maxFeatures",
                "maxgeowidth": "maxGeoWidth",
                "maxinterval": "maxInterval",
                "maxlength": "maxLength",
                "maxoverlapangle": "maxOverlapAngle",
                "maxscaledenom": "maxScaleDenom",
                "maxsize": "maxSize",
                "maxsubdivide": "maxSubdivide",
                "maxtemplate": "maxTemplate",
                "maxwidth": "maxWidth",
                "mimetype": "mimeType",
                "minarcs": "minArcs",
                "minboxsize": "minBoxSize",
                "mindistance": "minDistance",
                "minfeaturesize": "minFeatureSize",
                "mingeowidth": "minGeoWidth",
                "mininterval": "minInterval",
                "minscaledenom": "minScaleDenom",
                "minsize": "minSize",
                "minsubdivide": "minSubdivide",
                "mintemplate": "minTemplate",
                "minwidth": "minWidth",
                "outlinecolor": "outlineColor",
                "outlinecolorattribute": "outlineColorAttribute",
                "outlinewidth": "outlineWidth",
                "outputformat": "OutputFormat",
                "polaroffset": "polarOffset",
                "postlabelcache": "postLabelCache",
                "queryformat": "queryFormat",
                "querymap": "QueryMap",
                "repeatdistance": "repeatDistance",
                "scaledenom": "scaleDenom",
                "shadowcolor": "shadowColor",
                "shadowsize": "shadowSize",
                "shapepath": "shapePath",
                "sizeunits": "sizeUnits",
                "styleitem": "styleItem",
                "symbolscaledenom": "symbolScaleDenom",
                "symbolset": "symbolSet",
                "templatepattern": "templatePattern",
                "temppath": "tempPath",
                "tileindex": "tileIndex",
                "tileitem": "tileItem",
                "toleranceunits": "toleranceUnits",
                "patterns": "pattern",
                "metadata": "Metadata"
                }

    def makeSubElement(self, root, elements, key, upper=False):
        if "__type__" == key:
            return None
        logging.debug(f"processing key: {key}")
        if key in self.keyCases:
            keyx = self.keyCases[key]
        else:
            keyx = key
        el = etree.SubElement(root, keyx)

        # logging.debug(f"elements = {elements}")
        element = elements[key]
        #  if isinstance(element, plyplus.common.TokValue):
        #      el.text = escape(element).replace("'", "").replace('"', "")
        if key.find("color") > -1:
            el.set("red", str(element[0]))
            el.set("green", str(element[1]))
            el.set("blue", str(element[2]))
        elif (key.find("size") > -1 or key == 'keyspacing' or key == 'offset')\
                and isinstance(element, list):
            el.set("x", str(element[0]))
            el.set("y", str(element[1]))
        elif isinstance(element, list):
            if any(isinstance(el, list) for el in element):
                # lis = list(itertools.chain.from_iterable(element))
                lis = reduce(operator.add, element)
                # lis = reduce(operator.add, lis)
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
        for k in mapp[mapkey]:
            logging.debug(f"got legend key {k}")
            if "labels" == k:
                self.makeLabels(k, legend, mapp[mapkey][k])
            elif 'status' == k:
                legend.set("status", mapp[mapkey][k].upper())
            else:
                self.makeSubElement(legend, mapp[mapkey], k)
        legend = self.sortChildren(legend, legend)

    def makeLabels(self, s, class_, k):
        logging.debug(f"Making Labels: {s}, {class_}, {k}")
        labels = etree.SubElement(class_, "Label")
        for kx in k:
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
            layer = etree.SubElement(root, "Layer",
                                     name=l["name"].replace("\"", ""))
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
                    logging.debug(f"processing classes")

                    for s in l[key]:
                        class_ = etree.SubElement(layer, "Class")
                        for k in s.keys():
                            # logging.debug(f"got object {s[k]} for key {k}")
                            if k == 'name' or k == 'status':
                                class_.set(k, s[k].replace('"', '')
                                           .replace("'", ""))
                            elif k == 'styles':
                                st = s['styles']
                                logging.debug(f"Processing a style: {st}")

                                stEl = etree.SubElement(class_, "Style")
                                for sty in st:
                                    self.makeStyle(stEl, sty)
                                    stEl = self.sortChildren(stEl, stEl)
                            elif "labels" == k:
                                self.makeLabels(k, class_, s[k])
                            else:
                                self.makeSubElement(class_, s, k)
                        class_ = self.sortChildren(class_, class_)

                elif "metadata" == key:
                    meta = etree.SubElement(layer, "Metadata")
                    c = l[key]

                    for kx in c:
                        item = etree.SubElement(meta, "item",
                                                name=kx.replace("'", "")
                                                .replace("\"", ""))
                    item.text = c[kx].replace("'", "").replace("\"", "")
                elif "validation" == key:
                    validation = etree.SubElement(layer, "Validation")
                    for k in l["validation"]:
                        item = etree.SubElement(validation, "item",
                                                name=k[0].replace("'", "")
                                                .replace("\"", ""))
                        item.text = k[1].replace("'", "").replace("\"", "")

                elif "data" == key:
                    data = etree.SubElement(layer, "Data")
                    data.text = CDATA(l["data"][0])
                else:
                    self.makeSubElement(layer, l, key)
            layer = self.sortChildren(layer, layer)

    def makeStyle(self, element, style):
        for key in style.keys():
            logging.debug(f"processing style {key}")
            if key == 'symbol' and style[key] == 'dashed':
                # dashed lines are probably not a graphic symbol
                logging.debug("skipping dashed")
                continue
            self.makeSubElement(element, style, key)
        element = self.sortChildren(element, element)

    def makeQueryMaps(self, root, mapp, mapkey):
        qmap = etree.SubElement(root, "QueryMap")
        for k in mapp[mapkey]:
            if 'status' == k:
                qmap.set("status", mapp[mapkey][k])
            else:
                self.makeSubElement(qmap, mapp[mapkey], k)

    def makeWebs(self, root, mapp, mapkey):
        webs = etree.SubElement(root, "Web")
        for k in mapp[mapkey]:
            if "metadata" == k:
                meta = etree.SubElement(webs, "Metadata")
                c = mapp[mapkey]["metadata"]
                for kx in c:
                    item = etree.SubElement(meta, "item",
                                            name=kx.replace("'", "")
                                            .replace("\"", ""))
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
                    outputformat.set(k, fmt[k])
                else:
                    self.makeSubElement(outputformat, fmt, k)
            outputformat = self.sortChildren(outputformat, outputformat)

    def makeProjections(self, root, mapp, mapkey):
        # proj = etree.SubElement(root, "Projections")
        for k in mapp[mapkey]:
            el = etree.SubElement(root, "projection")
            el.text = str(" ".join(k)).replace("'", "").replace("\"", "")

    def makeScalebars(self, root, mapp, mapkey):
        scalebars = etree.SubElement(root, "ScaleBar")
        for k in mapp[mapkey]:
            logging.debug(f"Processing scalebar: {k}, ({mapkey})")
            if 'labels' == k:
                self.makeLabels(k, scalebars, mapp[mapkey][k])
            elif 'status' == k:
                scalebars.set('status', k)
            else:
                self.makeSubElement(scalebars, mapp[mapkey], k)
        scalebars = self.sortChildren(scalebars, scalebars)

    def makeConfig(self, root, mapp, mapkey):

        el = etree.SubElement(root, "Config")
        for k in mapp[mapkey].keys():
            item = etree.SubElement(el, "item",
                                    name=k.replace("'", "")
                                    .replace("\"", ""))
            item.text = mapp[mapkey][k]

    def makeSymbols(self, root, mapp, mapkey):
        logging.debug(f"Processing Symbol: ")
        for k in mapp[mapkey]:
            el = etree.SubElement(root, "Symbol")
            for d in k:
                if d == 'name':
                    el.set("name",
                           k['name'].replace("'", "").replace("\"", ""))
                elif d == 'type':
                    el.set("type",
                           k['type'].replace("'", "").replace("\"", ""))
                else:
                    self.makeSubElement(el, k, d)

    def sortChildren(self, root, new_root):
        temp = sorted(root, key=lambda x: attrgetter('tag')(x).lower())
        for x in temp:
            new_root.append(x)

        return new_root

    def __init__(self, input_file=None, input_string=None, output_file="",
                 width=2, tabs=False, expand_includes=True):
        if not input_file and not input_string:
            return
        if input_file:
            self.input = io.open(input_file, 'r', encoding="utf-8")
            self.output = output_file
            self.width = width
            self.tabs = tabs
            if self.output:
                sys.stdout = io.open(self.output, 'w', encoding="utf-8")
            else:
                # make sure that std out is utf-8 compliant
                # sys.stdout = codecs.getwriter('utf8')(sys.stdout)
                pass

            # parser = mappyfile.parser.Parser()
            self.root = etree.Element("Map",
                                      nsmap={
                                          None:
                                          "http://www.mapserver.org/mapserver"},
                                      name=input_file, version="5.6")
            # map_ = parser.parse_file(input_file)

            self.fix_nulls()
            mapp = mappyfile.utils.load(self.input,
                                        expand_includes=expand_includes)
            self.input.close()
        else:
            mapp = mappyfile.utils.loads(input_string,
                                         expand_includes=expand_includes)
            self.root = etree.Element("Map",
                                      nsmap={
                                          None:
                                          "http://www.mapserver.org/mapserver"},
                                      version="5.6")

        self.parse(mapp)

    def getroot(self):
        return self.root

    def setroot(self, root):
        self.root = root

    def parse(self, mapp):
        root = self.getroot()
        # logging.debug(f"got {mapp}")
        # mapp = mapp[0]
        for mapkey in mapp:
            logging.debug(f"got map key: {mapkey}")
            if "include" == mapkey:
                # import the file?
                pass
            elif "legend" == mapkey:
                self.makeLegend(root, mapp, mapkey)
            elif mapkey == 'layers':
                self.makeLayers(root, mapp, mapkey)
            elif mapkey == 'querymap':
                self.makeQueryMaps(root, mapp, mapkey)
            elif mapkey == 'web':
                self.makeWebs(root, mapp, mapkey)
            elif mapkey == 'outputformats':
                self.makeOutputFormats(root, mapp, mapkey)
            elif mapkey == 'projections':
                self.makeProjections(root, mapp, mapkey)
            elif mapkey == 'scalebar':
                self.makeScalebars(root, mapp, mapkey)
            elif mapkey == 'config':
                self.makeConfig(root, mapp, mapkey)
            elif mapkey == 'symbols':
                self.makeSymbols(root, mapp, mapkey)
            elif 'name' == mapkey:
                root.set("name", mapp['name'])
            elif 'status' == mapkey:
                root.set("status", mapp['status'].upper())
            else:
                self.makeSubElement(root, mapp, mapkey)

        # sort tag order to comply with XSD
        ms_ns = "http://www.mapserver.org/mapserver"
        root = self.sortChildren(root,
                                 etree.Element("Map",
                                               nsmap={None: ms_ns},
                                               # name=input_file,
                                               version="5.6"))
        self.map_root = root

    def print_map(self):
        print(etree.tostring(self.map_root, pretty_print=True))

    def fix_nulls(self):
        # convert "is not null" to " != null" and "is null" to " = NULL"
        buffer = ""
        for line in self.input:
            # FILTER ("roadno" not like 'C%' and "roadno"
            # becomes (not("roadno" like 'C%') and ...
            line = re.sub(r"([\w\"\'_%]+) not like ([\w\"\'_%]+)",
                          r"NOT \1 LIKE \2", line)

            line = line.replace("\\", "/")
            line = line.replace(" is not null", " != null")
            line = line.replace(" is null", " = null")
            buffer += line

        self.input = io.StringIO(buffer)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile",
                        type=str, help="the map file to be processed")
    parser.add_argument("-o", "--outputfile",
                        type=str,
                        help="the file to write output to (stdout if missing)",
                        default="")

    parser.add_argument("-d", "--debug", help="turn on debugging", default=False, action="store_true")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.info("Processing {}".format(args.inputfile))

    mapper = map_to_xml(args.inputfile,  output_file=args.outputfile)
    mapper.print_map()


if __name__ == "__main__":
    main()
