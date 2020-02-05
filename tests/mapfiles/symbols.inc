# ------------------- Start iShareMaps SYMBOLS --------------------

# Added SYMBOLS
# FUNDAMENTAL symbols
#POLYGON FILL TYPES
#vertical line
SYMBOL
    NAME "|line" 
    TYPE vector
    POINTS
        1 0
        1 2
    END
END
#horizontal line
SYMBOL
    NAME "-line"
    TYPE vector
    POINTS
        0 0.5
        1 0.5
    END
END
#diagonal line //
SYMBOL
  NAME "/line"
  TYPE vector
  POINTS
    0 1
    1 0
  END
END
SYMBOL
  NAME "HATCH"
  TYPE HATCH
END

#diagonal line \\
SYMBOL
  NAME "\line"
  TYPE vector
  POINTS
    0 0
    1 1
  END
END

SYMBOL
   NAME 'triangle'
   TYPE VECTOR
   FILLED TRUE
   POINTS 
     0 4
     2 0
     4 4
     0 4
   END
END

SYMBOL
   NAME 'square'
   TYPE VECTOR
   FILLED TRUE
   POINTS 0 0 0 1 1 1 1 0 0 0 END
END

SYMBOL
  NAME 'circle'
  TYPE ELLIPSE
  FILLED TRUE
  POINTS
    1 1
  END
END

#SYMBOL
#   NAME 'circle'
#   TYPE TRUETYPE
#   FONT "wingding"
#   CHARACTER "&#108;"
#   ANTIALIAS TRUE
#END

SYMBOL
    NAME 'dashed'
    TYPE ELLIPSE
    POINTS 1 1 END
    FILLED true
END

# --------------------
SYMBOL 
  NAME "continue"
  TYPE ELLIPSE
  FILLED TRUE
  POINTS 1 1 END
END

# --------------------

SYMBOL 
  NAME "dot"
  TYPE ELLIPSE
  FILLED TRUE
  POINTS 1 1 END
END

# --------------------

SYMBOL 
  NAME "dashed-line-short"
  TYPE ELLIPSE
  FILLED TRUE
  POINTS 1 1 END
END

# --------------------

SYMBOL 
  NAME "dashed-line-long"
  TYPE ELLIPSE
  FILLED TRUE
  POINTS 1 1 END
END

# --------------------

SYMBOL 
  NAME "dash-dot"
  TYPE ELLIPSE
  FILLED TRUE
  POINTS 1 1 END
END


### VECTOR symbols
# railway
SYMBOL
    NAME 'dcircle'
    TYPE ELLIPSE
    FILLED TRUE
    POINTS 1 1 END
END

#1
SYMBOL
  NAME "line-dots"
  TYPE ELLIPSE
  POINTS
    1 1
  END
  FILLED TRUE
END
SYMBOL
  NAME "line-dashed"
  TYPE ELLIPSE
  POINTS
    1 1
  END
END
SYMBOL
  NAME "line-dashed1"
  TYPE ELLIPSE
  POINTS
    1 1
  END
END
#7
SYMBOL
  NAME "line-dashed2"
  TYPE ELLIPSE
  POINTS
    1 1
  END
END
SYMBOL
  NAME "line-dashed3"
  TYPE ELLIPSE
  POINTS
    1 1
  END
END

SYMBOL # abwechselnd ein Linienstück und ein Punkt
  NAME "dash-dot1"
  TYPE ELLIPSE
  POINTS
    1 1
  END
  FILLED TRUE
END

SYMBOL # grenzsignatur mit gleichem Muster, aber einem Rechteck als Grundelement
  NAME "dash-dot2"
  TYPE VECTOR
  POINTS
    0 0
    1 0
    1 0.8
    0 0.8
    0 0
  END
  FILLED TRUE
END

SYMBOL
  NAME "dashed-spaced"
  TYPE VECTOR
  POINTS
    0 0
    0 0.6
    1 0.6
    1 0
    0 0
  END
  FILLED TRUE
END

SYMBOL # wie "rechteck-quer" aber mit einem typischen Linienmuster für Eisenbahnstrecken
  NAME "dashed-well"
  TYPE VECTOR
  POINTS
    0 0
    0 0.6
    1 0.6
    1 0
    0 0
  END
  FILLED TRUE
END

SYMBOL
  NAME "line"
  TYPE ELLIPSE
  POINTS
    1 1
  END
  FILLED TRUE
END
SYMBOL
  NAME "oval-flat"
  TYPE ELLIPSE
  POINTS
    2 1.25
  END
  FILLED TRUE
END
SYMBOL
  NAME "ellipse-vertical"
  TYPE ELLIPSE
  POINTS
    1.25 2
  END
  FILLED TRUE
END

SYMBOL
    NAME 'tie'
    TYPE TRUETYPE
    FONT "arial"
    CHARACTER "I"
END
