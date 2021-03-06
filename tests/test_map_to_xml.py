import unittest
import lxml.etree as ET
# from lxml.etree import QName
import os
import warnings
from maputils import map_to_xml
from maputils import xml_to_sld


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test


class Test_update_mapsource(unittest.TestCase):

    THIS_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

    def setUp(self):
        self.data_path = os.path.normpath(
            os.path.join(self.THIS_DIR, os.pardir, 'tests/mapfiles/'))
        # print("Data path: %s" % self.data_path)

    @ignore_warnings
    def test_read_map_file(self):
        obs = map_to_xml.map_to_xml(input_file='%s/andy.map' % self.data_path,
                                    expand_includes=False)
        root = obs.map_root
        # print(etree.tostring(root, pretty_print=True))
        self.assertTrue(root is not None)

    @ignore_warnings
    def test_polygon_mark_fill(self):
        sym_file = ('%s/polyfill.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        for layer in sldStore.layers:
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
        # print(sldStore.getLayer(layer).find(".//WellKnownName"))
        self.assertTrue(sldStore.getLayer(layer).find(".//WellKnownName") is not None)

    @ignore_warnings
    def test_read_symbols(self):
        sym_file = ('%s/symbols.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        for layer in sldStore.layers:
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)

        # print(sldStore.getLayer(layer).find(".//WellKnownName"))
        self.assertTrue(sldStore.getLayer(layer).find(".//WellKnownName") is not None)

    def read_map_file(self, file):
        obs = map_to_xml.map_to_xml(input_file=file)
        root = obs.map_root
        # print(ET.tostring(root, pretty_print=True))
        self.assertTrue(root is not None)
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        return sldStore

    @ignore_warnings
    def test_opacity(self):
        instr = """MAP
        LAYER
        NAME "test"
        TYPE LINE
        CLASSITEM "foo"
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
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
        good = False
        for css in sldStore.getLayer(layer).iter("CssParameter"):
            good = good or css.attrib['name'] == 'stroke-opacity'
        self.assertTrue(good)

    @ignore_warnings
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
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//Fill") is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//Stroke") is not None)

    @ignore_warnings
    def test_property_name(self):
        instr = """MAP
            LAYER
                NAME "test"
                TYPE POLYGON
                STATUS OFF
                CLASS
                        NAME "Comparison"
                        EXPRESSION "Comparison"
                        STYLE
                                COLOR 0 255 0
                                GAP 2
                                OPACITY 40
                                SIZE 3
                                SYMBOL dot
                        END
                        STYLE
                                OPACITY 40
                                OUTLINECOLOR 0 255 0

                        END

                END
                CLASSITEM "use"
            END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is not None)

    @ignore_warnings
    def test_like_filter(self):
        instr = """MAP
            LAYER
                NAME "loc_bs7666"
                TYPE POINT
                STATUS OFF
                CLASSITEM "blpu_classification_description"
                PROCESSING "CLOSE_CONNECTION=DEFER"
                METADATA
                    "__type__" "metadata"
                END
                VALIDATION
                    'qstring' ".*"
                END
                PROCESSING "CLOSE_CONNECTION=DEFER"
                UNITS METERS
                CLASS
                    NAME "Commercial"
                    EXPRESSION /^Commercial.*$/
                    STYLE
                        COLOR 0 0 255
                        SIZE 6
                        SYMBOL 'CIRCLE'
                    END

                END
                CLASS
                    NAME "Land"
                    EXPRESSION /^Land.*$/
                    STYLE
                        COLOR 153 255 51
                        SIZE 6
                        SYMBOL 'CIRCLE'
                    END

                END
            END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//PropertyIsLike") is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual("Commercial.*",
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ignore_warnings
    def test_expression_in_filter(self):
        instr = """MAP
            LAYER
                NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASS
                    NAME "Requiring Traffic Monitoring"
                    EXPRESSION ("[req_traffic_monitoriing]" eq "T" )
                    STYLE
                        COLOR 255 255 0
                        OPACITY 100
                        OUTLINECOLOR 255 255 0

                        WIDTH 3
                    END

                END
                CLASS
                    NAME "Hazardous Route - Yes"
                    EXPRESSION ( "[hazardous]" eq "T" )
                    STYLE
                        COLOR 255 0 0
                        OPACITY 100
                        OUTLINECOLOR 255 0 0

                        WIDTH 3
                    END

                END
                CLASS
                    NAME "Hazardous Route - No"
                    EXPRESSION ( "[hazardous]" eq "F" )
                    STYLE
                        COLOR 0 0 239
                        OPACITY 100
                        OUTLINECOLOR 0 0 239

                        WIDTH 3
                    END

                END
                PROCESSING "CLOSE_CONNECTION=DEFER"
                METADATA
                    "qstring_validation_pattern" ""
                    "__type__" "metadata"
                END
                PROCESSING "CLOSE_CONNECTION=DEFER"
                UNITS METERS
            END
        END"""

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        expected = [("req_traffic_monitoriing", 'T'),
                    ("hazardous", 'T'),
                    ("hazardous", 'F')]
        layerCount = 0
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//PropertyName") is not None)
            self.assertEqual(expected[layerCount][0],
                             sldStore.getLayer(layer).find(".//PropertyName").text)
            self.assertTrue(sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual(expected[layerCount][-1],
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ignore_warnings
    def test_process_expr(self):
        xsld = xml_to_sld.xml_to_sld()
        (classitem, expr, op) = xsld.process_regexpr('("[req_traffic_monitoriing]" eq "T" )', None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual("T", expr)
        self.assertEqual("PropertyIsEqualTo", op)
        (classitem, expr, op) = xsld.process_regexpr('("[req_traffic_monitoriing]" = "T" )', None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual("T", expr)
        self.assertEqual("PropertyIsEqualTo", op)
        (classitem, expr, op) = xsld.process_regexpr('("[req_traffic_monitoriing]" lt "T" )', None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual("T", expr)
        self.assertEqual("PropertyIsLessThan", op)

    @ignore_warnings
    def test_process_expr_with_or(self):
        xsld = xml_to_sld.xml_to_sld()
        filter = xsld.process_expr(
            ET.Element("Filter"),
            "",
            "( ( [alc_grade] eq 3A ) OR ( [alc_grade] eq 3B ) )")
        properties = filter.findall(".//PropertyName")
        self.assertEqual("alc_grade", properties[0].text)
        self.assertEqual("alc_grade", properties[1].text)
        literals = filter.findall(".//Literal")
        self.assertEqual("3A", literals[0].text)
        self.assertEqual("3B", literals[1].text)

    @ignore_warnings
    def test_list_expressions(self):
        instr = """MAP
            LAYER
                    NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASSITEM ian
                CLASS
                    NAME "Grade 3A or 3B"
                    EXPRESSION {Grade 3a,Grade 3b}
                    STYLE
                        COLOR 255 128 64
                        OPACITY 50
                        OUTLINECOLOR 255 128 64

                    END

                END
            END
        END"""

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is not None)
            properties = sldStore.getLayer(layer).findall(".//PropertyName")
            self.assertTrue(properties is not None)
            self.assertEqual("ian", properties[0].text)
            self.assertEqual("ian", properties[1].text)
            literals = sldStore.getLayer(layer).findall(".//Literal")
            self.assertTrue(literals is not None)
            self.assertEqual("Grade 3a", literals[0].text)
            self.assertEqual("Grade 3b", literals[1].text)
