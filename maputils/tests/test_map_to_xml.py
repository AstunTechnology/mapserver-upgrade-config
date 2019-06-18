from __future__ import print_function
# import pytest
import lxml.etree as ET
# from lxml.etree import QName
import os
from maputils import map_to_xml
from maputils import xml_to_sld


class Test_update_mapsource:

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    def setup_method(self, method):
        self.data_path = os.path.normpath(
            os.path.join(self.THIS_DIR, os.pardir, 'tests/mapfiles/'))

    def test_read_map_file(self):
        obs = map_to_xml.map_to_xml(input_file='%s/andy.map' % self.data_path,
                                    expand_includes=False)
        root = obs.map_root
        # print(etree.tostring(root, pretty_print=True))
        assert(root is not None)

    def test_opacity(self):
        instr = """MAP
        LAYER
        NAME "test"
        TYPE LINE
        CLASS
            NAME "class 1"
                EXPRESSION "1"
                STYLE
                COLOR 222 100 199
                OPACITY 50
            END
            END
            END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            print("layer", layer)
            ET.dump(sldStore.getLayer(layer))
        assert(layer is not None)
        good = False
        for css in sldStore.getLayer(layer).iter("CssParameter"):
            good = good or css.attrib['name'] == 'stroke-opacity'
        assert(good)

    def test_marks(self):
        instr = """MAP
        LAYER
        NAME "test"
        TYPE POINT
        CLASS
        NAME ""
            STYLE
                COLOR 156 72 12
                SIZE 6
                SYMBOL "circle"
                WIDTH 4
            END
            STYLE
                OUTLINECOLOR 156 72 12
                SIZE 6
                SYMBOL "circle"
                WIDTH 2
            END
            END
            END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            print("layer", layer)
            ET.dump(sldStore.getLayer(layer))
        assert(sldStore.getLayer(layer) is not None)
        assert(sldStore.getLayer(layer).find("Fill") != -1)
        assert(sldStore.getLayer(layer).find("Stroke") != -1)