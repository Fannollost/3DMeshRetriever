from enum import Enum
from math import pi
import numpy as np

class globalShapeDescriptorTypes(Enum):
    SURFACE_AREA = "Surface Area"
    COMPACTNESS = "Compactness"
    RECTANGULARITY = "Rectangularity"
    DIAMETER = "Diameter"
    CONVEXITY = "Convexity"
    ECCENTRICITY = "Eccentricity"
    VOLUME = "Volume"

globalShapeDescriptorTypesSizes = { globalShapeDescriptorTypes.SURFACE_AREA.value : 1, globalShapeDescriptorTypes.COMPACTNESS.value : 1,
                                    globalShapeDescriptorTypes.RECTANGULARITY.value : 1, globalShapeDescriptorTypes.DIAMETER.value : 1,
                                    globalShapeDescriptorTypes.CONVEXITY.value : 1, globalShapeDescriptorTypes.ECCENTRICITY.value : 1,
                                    globalShapeDescriptorTypes.VOLUME.value: 1}

class propertyDescriptorTypes(Enum):
    A3 = "A3"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    D4 = "D4"

histogramLimits =  { propertyDescriptorTypes.A3.value : pi, propertyDescriptorTypes.D1.value : np.sqrt(3) / 2, propertyDescriptorTypes.D2.value : np.sqrt(3), propertyDescriptorTypes.D3.value : np.sqrt(3/4) , propertyDescriptorTypes.D4.value:(1/6)**(1/3)}

weight = { propertyDescriptorTypes.A3.value: 1, propertyDescriptorTypes.D1.value : 1, propertyDescriptorTypes.D2.value : 1, propertyDescriptorTypes.D3.value : 1,
                     propertyDescriptorTypes.D4.value : 1, globalShapeDescriptorTypes.SURFACE_AREA.value : 1, globalShapeDescriptorTypes.VOLUME.value : 1,
                     globalShapeDescriptorTypes.COMPACTNESS.value : 1, globalShapeDescriptorTypes.RECTANGULARITY.value : 1, globalShapeDescriptorTypes.CONVEXITY.value:1,
                     globalShapeDescriptorTypes.DIAMETER.value : 1, globalShapeDescriptorTypes.ECCENTRICITY.value : 5 }