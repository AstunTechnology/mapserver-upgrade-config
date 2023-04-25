import unittest
import lxml.etree as ET
# from lxml.etree import QName
import os
import warnings
import logging
from maputils import map_to_xml
from maputils import xml_to_sld
from xmldiff import main


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)

    return do_test


class Test_update_mapsource(unittest.TestCase):

    THIS_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(level=logging.DEBUG)

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
    def test_read_sql(self):
        map = r"""
        MAP
          LAYER
    NAME "PlanApp_2000_2009"
    STATUS OFF
    TYPE POLYGON
    OPACITY 20
    DATA "wkb_geometry from (select * FROM PLANNING_SCHEMA.allplanning_2000_onwards_polys_and_data where \"CaseFullRef\" < '09/P/99999') as foo using unique ogc_fid using srid=27700"
    TOLERANCEUNITS PIXELS
    METADATA
      ows_title "PlanApp_2000_2009"
      ows_abstract "PlanApp_2000_2009"
          END
    VALIDATION
      qstring '.'

    END
    CLASS
      NAME ""
      STYLE
        COLOR 249 014 255
      END
    END
  END
  END
        """
        obs = map_to_xml.map_to_xml(input_string=map)
        root = obs.map_root
        self.assertTrue(root is not None)
        ET.dump(root, pretty_print=True)
        logging.debug(root.find(".//Data").text)
        self.assertTrue('"CaseFullRef"' in root.find(".//Data").text)

    @ignore_warnings
    def test_polygon_mark_fill(self):
        sym_file = ('%s/polyfill.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        for layer in sldStore.layers:
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
        # print(sldStore.getLayer(layer).find(".//WellKnownName"))
        self.assertTrue(
            sldStore.getLayer(layer).find(".//WellKnownName") is not None)

    @ignore_warnings
    def test_read_symbols(self):
        sym_file = ('%s/symbols.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        for layer in sldStore.layers:
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)

        # print(sldStore.getLayer(layer).find(".//WellKnownName"))
        self.assertTrue(
            sldStore.getLayer(layer).find(".//WellKnownName") is not None)

    def read_map_file(self, file):
        obs = map_to_xml.map_to_xml(input_file=file)
        root = obs.map_root
        # print(ET.tostring(root, pretty_print=True))
        self.assertTrue(root is not None)
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        return sldStore

    @ignore_warnings
    def test_bracketed_expressions(self):
        instr = """MAP
        LAYER
        NAME "test"
        TYPE LINE
        CLASSITEM "foo"
        CLASS
            NAME "Single Tree Order status unknown"
            EXPRESSION ("[tag_desc]" = "Single Tree Order (Status Unknown)")
            STYLE
                SYMBOL "triangle"
                COLOR 0 255 0
                SIZE 10
            END
        END
        END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # print("layer", layer)
            ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
            literal = sldStore.getLayer(layer).find('.//Literal')
            self.assertEquals("Single Tree Order (Status Unknown)", literal.text)

    @ignore_warnings
    def test_bracketed_expressions2(self):
        instr = """MAP
        LAYER
                DATA "wkb_geometry from (select upper(substr(feature_type,1,1) || substr(gully_owner,1,2) || substr(COALESCE(critical, 'No'),1,1) || CASE (COALESCE(priority_route,'')) WHEN '' THEN 'N' ELSE 'Y' END) AS rendition, gully_id::character varying(6) as gully_ref, * from highways.highway_gullies where status = 'Live') as foo using unique ogc_fid using srid=27700"
                VALIDATION
                         qstring '.'
                END
                NAME "highway_gullies"
                STATUS OFF
                TYPE POINT
                UNITS METERS
                LABELITEM "gully_id"
                CLASS
                        NAME "Housing Gully"
                        EXPRESSION ("[rendition]" = "GHONY" or "[rendition]" = "GHOYY" or "[rendition]" = "GHONN" or "[rendition]" = "GHOYN" )
                        STYLE
                                SYMBOL "square"
                                OUTLINECOLOR 0 128 0
                                OUTLINEWIDTH 2
                                SIZE 7
                        END
                        LABEL
                                TYPE TrueType
                                FONT "arialbd"
                                COLOR 0 128 0
                                OUTLINECOLOR 255 255 255
                                SIZE 8
                                POSITION AUTO
                                MAXSCALEDENOM 2000
                                POSITION AUTO
                        END
                END
        END
        END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        expected = ["GHONY",
                    "GHOYY",
                    "GHONN",
                    "GHOYN"]
        for layer in sldStore.layers:
            # print("layer", layer)
            ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
            filter = sldStore.getLayer(layer).find('.//Filter')
            exprs = filter.findall('.//Literal')
            for expect, exp in zip(expected, exprs):
                self.assertEquals(expect, exp.text)

    @ ignore_warnings
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

    @ ignore_warnings
    def test_legend(self):
        """make sure fix for issue #11 works"""
        instr = """MAP
                    LEGEND
                        IMAGECOLOR 255 255 255
                        KEYSIZE 20 10
                        KEYSPACING 5 5
                        LABEL
                            SIZE MEDIUM
                            TYPE BITMAP
                            BUFFER 0
                            COLOR 0 0 0
                            FORCE FALSE
                            MINDISTANCE -1
                            MINFEATURESIZE -1
                            OFFSET 0 0
                            PARTIALS TRUE
                        END
                        POSITION LL
                        STATUS OFF
                    END
                    QUERYMAP
                        COLOR 255 255 0
                        SIZE -1 -1
                        STATUS OFF
                        STYLE HILITE
                    END

                    SCALEBAR
                        COLOR 0 0 0
                        IMAGECOLOR 255 255 255
                        INTERVALS 4
                        LABEL
                        SIZE MEDIUM
                        TYPE BITMAP
                        BUFFER 0
                        COLOR 0 0 0
                        FORCE FALSE
                        MINDISTANCE -1
                        MINFEATURESIZE -1
                        OFFSET 0 0
                        PARTIALS TRUE
                        END
                        POSITION LL
                        SIZE 200 3
                        STATUS OFF
                        STYLE 0
                        UNITS MILES
                    END
                END"""
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        # print(ET.tostring(root, pretty_print=True))
        self.assertTrue(root is not None)
        legend = root.find(".//Legend")
        self.assertTrue(legend)
        labels = legend.find("Label")
        self.assertTrue(labels)
        qMap = root.find(".//QueryMap")
        self.assertTrue(qMap)
        color = qMap.find("color")
        self.assertTrue(color is not None)
        scale = root.find(".//ScaleBar")
        self.assertTrue(scale)
        labels = scale.find("Label")
        self.assertTrue(labels)

    @ ignore_warnings
    def test_graphic_stroke(self):
        instr = """MAP
            LAYER
                NAME "prow"
                TYPE LINE
                STATUS OFF
                CLASS
                NAME "Metro"
                #           EXPRESSION  ("[tag]"  = "METR" )
                EXPRESSION ("[tag]"  = "METR" )
                STYLE
                    COLOR 222 134 0
                    WIDTH 2
                END
                STYLE
                    SYMBOL "|line"
                    COLOR 222 134 0
                    WIDTH 2
                    SIZE 6
                    GAP -4
                    END
                END
            END
        END
        """
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        # ET.dump(root)
        self.assertEquals(2, len(root.findall(".//Style")))
        # print("------------------------------------------")
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # print("layer", layer)
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(layer is not None)
            style = sldStore.getLayer(layer)
            self.assertEqual(2, len(style.findall(".//LineSymbolizer")))
            symbolizer = style.findall(".//LineSymbolizer")[1]
            # ET.dump(symbolizer)
            self.assertTrue(symbolizer.find("./Stroke/CssParameter[@name='stroke-dasharray']") is not None)
            exp_tree = ET.parse(f"{self.THIS_DIR}/mapfiles/expected.sld")
            diff = main.diff_trees(exp_tree, symbolizer)
            if len(diff) != 0:
                print(f"Diff:\n {diff}")
            self.assertTrue(0 == len(diff))

    @ ignore_warnings
    def test_dashes(self):
        sym_file = ('%s/dashes.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        layer = 'prow'
        # ET.dump(sldStore.getLayer(layer))
        style = sldStore.getLayer(layer)
        # ET.dump(style)
        self.assertEqual(3, len(style.findall(".//CssParameter[@name='stroke-dasharray']")))
        sym_file = ('%s/dashes_2.map' % self.data_path)
        sldStore = self.read_map_file(sym_file)
        layer = 'prow'
        # ET.dump(sldStore.getLayer(layer))
        style = sldStore.getLayer(layer)

    @ ignore_warnings
    def test_raster(self):
        instr = """MAP
        LAYER
            NAME "air_quality"
            DATA "AirQuality/Dudley_Classified_NoPalette.tif"
            TYPE RASTER
            STATUS OFF
            CLASSITEM "[pixel]"
            CLASS
                NAME "36-40 microgrammes/cubic metre"
                EXPRESSION ([pixel] < 100)
                STYLE
                    COLOR 255 255 0
                END
            END
            CLASS
                NAME "40-44 microgrammes/cubic metre"
                EXPRESSION ([pixel] < 150)
                STYLE
                    COLOR 255 150 0
                END
            END
            CLASS
                NAME "44-60 microgrammes/cubic metre"
                EXPRESSION ([pixel] < 175)
                STYLE
                    COLOR 255 75 0
                END
            END
            CLASS
                NAME "Over 60 microgrammes/cubic metre"
                EXPRESSION ([pixel] < 225)
                STYLE
                    COLOR 200 0 0
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
            self.assertTrue(
                layer.find(".//ColorMap") is not None)
            self.assertTrue(
                layer.find(".//ColorMapEntry") is not None)
            expected = ['100', '150', '175', '225']
            for _i, cme in enumerate(sldStore.getLayer(layer).iterfind(".//ColorMapEntry")):
                self.assertEquals(expected[_i], cme.attrib['quantity'])

    @ ignore_warnings
    def test_marks(self):
        instr = """MAP
        LAYER
        NAME "test"
        TYPE POINT
        CLASS
        NAME ""
            STYLE
                OUTLINECOLOR 156 72 12
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
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(sldStore.getLayer(layer).find(".//Fill") is not None)

            stroke = sldStore.getLayer(layer).find(".//Stroke")
            self.assertTrue(stroke is not None)
            # issue 40 - don't double set stroke-width and Size
            good = False
            for css in stroke.iter("CssParameter"):
                good = good or css.attrib['name'] == 'stroke-width' or css.attrib['name'] == 'stroke-opacity'
            self.assertTrue(good)
            self.assertTrue(sldStore.getLayer(layer).find(".//Size") is not None)

    @ ignore_warnings
    def test_marks_sizes(self):
        instr = """MAP
        LAYER
            NAME "test"
            TYPE POINT
            CLASS
                NAME "Postal Address"
                EXPRESSION "Y"
                MAXSCALEDENOM 5000
                STYLE
                    SYMBOL "circle"
                    OUTLINECOLOR 0 0 0
                    COLOR 0 128 0
                    SIZE 7
                    OPACITY 80
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
            self.assertTrue(sldStore.getLayer(layer).find(".//Fill") is not None)

            stroke = sldStore.getLayer(layer).find(".//Stroke")
            self.assertTrue(stroke is not None)
            # issue 40 - don't double set stroke-width and Size
            bad = False
            for css in stroke.iter("CssParameter"):
                bad = bad or css.attrib['name'] == 'stroke-width'
            self.assertFalse(bad)
            self.assertTrue(sldStore.getLayer(layer).find(".//Size") is not None)

    @ ignore_warnings
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
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is
                not None)

    @ ignore_warnings
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
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsLike") is not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual("Commercial.*",
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ ignore_warnings
    def test_like2_filter(self):
        instr = """MAP
            LAYER
                NAME "loc_bs7666"
                TYPE POINT
                CLASS
                    NAME "Commercial"
                    EXPRESSION ('[owner]' ~* 'Dudley MBC.*$')
                    STYLE
                        COLOR 0 0 255
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
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsLike") is not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual(".*Dudley MBC.*",
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ ignore_warnings
    def test_like3_filter(self):
        instr = """MAP
            LAYER
                NAME "loc_bs7666"
                TYPE POINT
                CLASS
                    NAME "Commercial"
                    EXPRESSION ('[owner]' ~ 'Dudley MBC.*$')
                    STYLE
                        COLOR 0 0 255
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
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsLike") is not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual(".*Dudley MBC.*",
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ ignore_warnings
    def test_outlinecolor_in_line(self):
        instr = """
        MAP
            LAYER
                NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASS
                    NAME "Requiring Traffic Monitoring"
                    EXPRESSION ("[req_traffic_monitoriing]" eq "T" )
                    STYLE
                        OPACITY 100
                        OUTLINECOLOR 255 255 0
                        WIDTH 3
                    END
                END
            END
        END"""

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            ET.dump(sldStore.getLayer(layer))

    @ ignore_warnings
    def test_expression_in_filter(self):
        instr = """
        MAP
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
        expected = [("req_traffic_monitoriing", 'T'), ("hazardous", 'T'),
                    ("hazardous", 'F')]
        layerCount = 0
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is
                not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyName") is not None)
            self.assertEqual(
                expected[layerCount][0],
                sldStore.getLayer(layer).find(".//PropertyName").text)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//Literal") is not None)
            self.assertEqual(expected[layerCount][-1],
                             sldStore.getLayer(layer).find(".//Literal").text)

    @ ignore_warnings
    def test_process_expr(self):
        xsld = xml_to_sld.xml_to_sld()
        (classitem, expr,
         op) = xsld.process_regexpr('("[req_traffic_monitoriing]" eq "T" )',
                                    None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual('"T"', expr)
        self.assertEqual("PropertyIsEqualTo", op)
        (classitem, expr,
         op) = xsld.process_regexpr('("[req_traffic_monitoriing]" = "T" )',
                                    None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual('"T"', expr)
        self.assertEqual("PropertyIsEqualTo", op)
        (classitem, expr,
         op) = xsld.process_regexpr('("[req_traffic_monitoriing]" lt "T" )',
                                    None)
        self.assertEqual("req_traffic_monitoriing", classitem)
        self.assertEqual('"T"', expr)
        self.assertEqual("PropertyIsLessThan", op)

    @ ignore_warnings
    def test_process_expr_with_space(self):
        xsld = xml_to_sld.xml_to_sld()
        (classitem, expr,
         op) = xsld.process_regexpr('("[tag_desc]"  = "Group Order (Not Confirmed)" )',
                                    None)
        self.assertEqual("tag_desc", classitem)
        self.assertEqual('"Group Order (Not Confirmed)"', expr)
        self.assertEqual("PropertyIsEqualTo", op)

    @ ignore_warnings
    def test_process_expr_with_or(self):
        xsld = xml_to_sld.xml_to_sld()
        filter = xsld.process_expr(
            ET.Element("Filter"), "",
            "( ( [alc_grade] eq 3A ) OR ( [alc_grade] eq 3B ) )")
        ET.dump(filter)
        properties = filter.findall(".//PropertyName")
        self.assertEqual("alc_grade", properties[0].text)
        self.assertEqual("alc_grade", properties[1].text)
        literals = filter.findall(".//Literal")
        self.assertEqual("3A", literals[0].text)
        self.assertEqual("3B", literals[1].text)

    @ ignore_warnings
    def test_process_expr_with_and(self):
        xsld = xml_to_sld.xml_to_sld()
        filter = xsld.process_expr(
            ET.Element("Filter"), "",
            "( ( [alc_grade] eq 3A ) AND ( [alc_grade] eq 3B ) )")
        # ET.dump(filter)
        properties = filter.findall(".//PropertyName")
        self.assertEqual("alc_grade", properties[0].text)
        self.assertEqual("alc_grade", properties[1].text)
        literals = filter.findall(".//Literal")
        self.assertEqual("3A", literals[0].text)
        self.assertEqual("3B", literals[1].text)

    @ ignore_warnings
    def test_broken_expressions(self):
        instr = """MAP
        LAYER
        DATA "wkb_geometry from (select * from osmm.topographicline) as foo using unique ogc_fid using srid=27700"
        METADATA
             "qstring_validation_pattern" "."
        END
        NAME "mastermap_outline"
        STATUS OFF
        TYPE LINE
        UNITS METERS
        #       LABELITEM "site_ref"
        CLASS
            NAME "Current OS Mapping"
            EXPRESSION ([featurecode] lt 10112 OR [featurecode] gt 10118)
            STYLE
                OUTLINECOLOR 1 191 254
                WIDTH 0.8
                #               WIDTH 0.9
                MAXSCALEDENOM 5000
            END
        END
    END
        END"""

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsLessThan") is
                not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsGreaterThan") is
                not None)
            properties = sldStore.getLayer(layer).findall(".//PropertyName")
            self.assertTrue(properties is not None)
            self.assertEqual("featurecode", properties[0].text)
            self.assertEqual("featurecode", properties[1].text)
            literals = sldStore.getLayer(layer).findall(".//Literal")
            self.assertTrue(literals is not None)
            self.assertEqual("10112", literals[0].text)
            self.assertEqual("10118", literals[1].text)

    @ ignore_warnings
    def test_complex_in_expressions(self):
        instr = """MAP
            LAYER
                    NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASS
                    NAME "Grade 3A or 3B"
                    EXPRESSION ("[status_code]" IN "LBI,LBII*,LBD")
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
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is
                not None)
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsLike") is
                not None)
            properties = sldStore.getLayer(layer).findall(".//PropertyName")
            self.assertTrue(properties is not None)
            self.assertEqual("status_code", properties[0].text)
            self.assertEqual("status_code", properties[1].text)
            self.assertEqual("status_code", properties[2].text)
            literals = sldStore.getLayer(layer).findall(".//Literal")
            self.assertTrue(literals is not None)
            self.assertEqual("LBI", literals[0].text)
            self.assertEqual("LBII*", literals[1].text)
            self.assertEqual("LBD", literals[2].text)

    @ ignore_warnings
    def test_simple_in_expressions(self):
        instr = """MAP
            LAYER
                    NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASS
                    NAME "Grade 3A or 3B"
                    EXPRESSION ("[status_code]" IN "LBI,LBII,LBD")
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
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is
                not None)
            properties = sldStore.getLayer(layer).findall(".//PropertyName")
            self.assertTrue(properties is not None)
            self.assertEqual("status_code", properties[0].text)
            self.assertEqual("status_code", properties[1].text)
            self.assertEqual("status_code", properties[2].text)
            literals = sldStore.getLayer(layer).findall(".//Literal")
            self.assertTrue(literals is not None)
            self.assertEqual("LBI", literals[0].text)
            self.assertEqual("LBII", literals[1].text)
            self.assertEqual("LBD", literals[2].text)

    @ ignore_warnings
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
            self.assertTrue(
                sldStore.getLayer(layer).find(".//PropertyIsEqualTo") is
                not None)
            properties = sldStore.getLayer(layer).findall(".//PropertyName")
            self.assertTrue(properties is not None)
            self.assertEqual("ian", properties[0].text)
            self.assertEqual("ian", properties[1].text)
            literals = sldStore.getLayer(layer).findall(".//Literal")
            self.assertTrue(literals is not None)
            self.assertEqual("Grade 3a", literals[0].text)
            self.assertEqual("Grade 3b", literals[1].text)

    @ ignore_warnings
    def test_dashed_paths2(self):
        instr = """
        MAP
            LAYER
                NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASSITEM ian
            CLASS
      NAME "Carer/Support to Carer"
      EXPRESSION "SSCA"
      STYLE
        SYMBOL "circle"
        OUTLINECOLOR 0 0 255
        SIZE 5.5
      END
    END
            END
        END
        """

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)

    @ ignore_warnings
    def test_dashed_paths(self):
        instr = """
        MAP
            LAYER
                NAME "tra_edu_dcc_hazroutes"
                TYPE LINE
                STATUS OFF
                CLASSITEM ian
                CLASS
                    NAME "Footpath"
                    EXPRESSION "Footpath"
                    LABEL
                        TYPE TRUETYPE
                        ANGLE AUTO
                        COLOR 255 128 0

                        FONT verdana
                        OUTLINECOLOR 255 255 255
                        OUTLINEWIDTH 1
                        SIZE 6
                        MAXSCALEDENOM 15000
                    END
                    STYLE
                        COLOR 255 128 0
                        PATTERN 5 5 END
                        SIZE 5
                        SYMBOL dashed
                    END
                END
            END
        END
        """

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)

    @ ignore_warnings
    def test_rotation(self):
        instr = """
        MAP
        LAYER
    DATA "wkb_geometry from (select * from osmm.vew_carto_text_overlay) as foo using unique ogc_fid using srid=27700"
    METADATA
       "qstring_validation_pattern" "."
    END
    NAME "mastermap_carto_text"
    STATUS OFF
    TYPE POINT
    UNITS METERS
    LABELITEM "textstring"
    CLASS
      MAXSCALEDENOM 2500
      STYLE
#       OUTLINECOLOR 143 143 143
#       WIDTH 1

      END
      LABEL
        TYPE TrueType
        FONT "arialbd"
        COLOR 1 191 254
#       OUTLINECOLOR 255 255 255
        ANGLE [orientation]
        SIZE 7
        POSITION cr
      END
    END
  END
        END
        """

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            rot = sldStore.getLayer(layer).find(".//Rotation")
            # ET.dump(rot)
            self.assertTrue(rot.find(".//PropertyName") is not None)

    @ ignore_warnings
    def test_two_styles(self):
        map = """
        MAP
            LAYER
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE LINE
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "New Stop"
                    EXPRESSION "New Station"
                    STYLE
                        COLOR 0 0 0
                        WIDTH 5
                    END
                    STYLE
                        COLOR 200 22 25
                        WIDTH 4
                    END
                    LABEL
                        TYPE TrueType
                        FONT "arialbd"
                        COLOR 200 22 25
                        OUTLINECOLOR 255 255 255
                        SIZE 8
                        POSITION AUTO
                    END
                END
            END
        END
        """
        obs = map_to_xml.map_to_xml(input_string=map)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertEqual(2, len(sldStore.getLayer(layer).findall(".//LineSymbolizer")))

    @ ignore_warnings
    def test_hatching_graphic_rotate(self):
        map = """
        MAP
            LAYER
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE POLYGON
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "Building Height 0-10m"
                    EXPRESSION ([code]>0 AND [code]<10 )
                    STYLE
                        SYMBOL "HATCH"
                        COLOR 0 255 64
                        SIZE 10
                        ANGLE 45
                        WIDTH 2
                    END
                    STYLE
                        OUTLINECOLOR 0 255 64
                        WIDTH 2
                    END
                END
            END
        END
        """
        maps = [map, map.replace('ANGLE 45', 'ANGLE 90'), map.replace('ANGLE 45', 'ANGLE 135')]
        expected_symbol = ['/line', '|line', '\\line']
        for map, symb in zip(maps, expected_symbol):
            obs = map_to_xml.map_to_xml(input_string=map)
            root = obs.map_root
            sldStore = xml_to_sld.xml_to_sld("", root=root)
            for layer in sldStore.layers:
                self.assertTrue(sldStore.getLayer(layer) is not None)
                ET.dump(sldStore.getLayer(layer))
                gf = sldStore.getLayer(layer).findall(".//GraphicFill")
                self.assertEquals(1, len(gf))
                self.assertEquals(2, len(sldStore.getLayer(layer).findall(".//Fill")))
                self.assertEquals(2, len(sldStore.getLayer(layer).findall(".//Stroke")))
                self.assertIsNotNone(gf[0].find(".//Stroke"))
                rot = sldStore.getLayer(layer).find(".//Rotation")
                self.assertEquals(None, rot)
                self.assertEqual(symb, gf[0].find(".//WellKnownName").text)

    @ ignore_warnings
    def test_hatching_graphic_fill(self):
        map = """
        MAP
            LAYER
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE POLYGON
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "Building Height 0-10m"
                    EXPRESSION ([code]>0 AND [code]<10 )
                    STYLE
                        SYMBOL "HATCH"
                        COLOR 0 255 64
                        SIZE 10
                        ANGLE 45
                        WIDTH 2
                    END
                    STYLE
                        OUTLINECOLOR 0 255 64
                        WIDTH 2
                    END
                END
            END
        END
        """
        obs = map_to_xml.map_to_xml(input_string=map)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer) is not None)
            # ET.dump(sldStore.getLayer(layer))
            self.assertEquals(1, len(sldStore.getLayer(layer).findall(".//GraphicFill")))
            self.assertEquals(2, len(sldStore.getLayer(layer).findall(".//Fill")))
            self.assertEquals(2, len(sldStore.getLayer(layer).findall(".//Stroke")))

    @ ignore_warnings
    def test_pattern(self):
        map = """
        MAP
            LAYER
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE POLYGON
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "Postcode Sector 0"
                    EXPRESSION ('[postcode]' ~* '0..$')
                    STYLE
                        OUTLINECOLOR 255 0 0
                        WIDTH 0.5
                    END
                    STYLE
                        COLOR 255 0 0
                        OPACITY 40
                    END
                END
            END
        END
        """
        obs = map_to_xml.map_to_xml(input_string=map)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertEquals('.*0..', sldStore.getLayer(layer).find(".//Literal").text)

    @ ignore_warnings
    def test_web_process_present(self):
        obs = map_to_xml.map_to_xml(input_file='%s/webproc.map' % self.data_path,
                                    expand_includes=False)
        root = obs.map_root
        # ET.dump(root, pretty_print=True)
        self.assertTrue(root is not None)
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            self.assertTrue(sldStore.getLayer(layer))

    @ ignore_warnings
    def test_nulls(self):
        instr = """
            MAP
            LAYER
                METADATA
                    "qstring_validation_pattern" "."
                END
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE POINT
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "Unknown"
                    EXPRESSION ("[road_status_code]"  = "" )
                    STYLE
                        OUTLINECOLOR 0 0 0
                        WIDTH 3
                        PATTERN
                        6 4
                        END
                    END
                END
            END
            END
            """

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertIsNotNone(sldStore.getLayer(layer).find('.//Filter/PropertyIsNull'))

    @ ignore_warnings
    def test_label_position(self):
        instr = """
            MAP
            LAYER
                METADATA
                    "qstring_validation_pattern" "."
                END
                NAME "mastermap_carto_text"
                STATUS OFF
                TYPE POINT
                UNITS METERS
                LABELITEM "textstring"
                CLASS
                    NAME "Unknown"
                    EXPRESSION ("[road_status_code]"  = "" )
                    STYLE
                        OUTLINECOLOR 0 0 0
                        WIDTH 3
                    END
                    LABEL
                        COLOR 255 102 102
                        OUTLINECOLOR 255 255 255
                        FONT "arialbd"
                        TYPE truetype
                        SIZE 12
                    END
                END
            END
            END
            """

        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        # ET.dump(root)
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            # ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            self.assertIsNotNone(sldStore.getLayer(layer).find('.//AnchorPointX'))
            self.assertIsNotNone(sldStore.getLayer(layer).find('.//Label/PropertyName'))

    @ignore_warnings
    def test_external_image(self):
        instr = """
        MAP
            SYMBOL
            NAME "tree"
            TYPE PIXMAP
            IMAGE "D:/mapserver/shared/symbols/Legend/landuse_deciduous_green.png"
        END
            LAYER
                NAME "ancient_woodland_2034"
                TYPE POLYGON
                STATUS OFF
                CLASS
                    NAME ""
                    STYLE
                        COLOR 83 104 64
                        SIZE 10
                        SYMBOL "tree"
                        WIDTH 10
                    END
                    STYLE
                        OUTLINECOLOR 0 0 0
                    END
                END
                INCLUDE "sdw.inc"
                CONNECTIONTYPE POSTGIS
                DATA "wkb_geometry from (select * FROM draft_lp_2019_2034_schema.ancient_woodland) as foo using unique ogc_fid using srid=27700"
                METADATA
                    "ows_title" ""
                    "ows_abstract" ""
                END
                TOLERANCEUNITS PIXELS
            END
        END
        """
        obs = map_to_xml.map_to_xml(input_string=instr)
        root = obs.map_root
        # ns = root.nsmap  # {'xlink': 'http://www.w3.org/1999/xlink'}
        ET.dump(root)
        sldStore = xml_to_sld.xml_to_sld("", root=root)
        for layer in sldStore.layers:
            ET.dump(sldStore.getLayer(layer))
            self.assertTrue(sldStore.getLayer(layer) is not None)
            res = sldStore.getLayer(layer).find('.//OnlineResource')
            self.assertIsNotNone(res)
            self.assertEquals(res.attrib.get('{http://www.w3.org/1999/xlink}href'),
                              'file:///D:/mapserver/shared/symbols/Legend/landuse_deciduous_green.png')
