from enum import Enum

class dataTypes(Enum):
    CLASS = "Class"
    AMOUNT_FACES = "Amount of Faces"
    AMOUNT_VERTICES = "Amount of Vertices"
    BARY_CENTER =  "Barycenter of pointcloud"
    MAX_SIZE = "Biggest axis boundingbox"
    SIZE = "Size"
    DISTANCE_ORIGIN = "Barycenter distance to origin"

dataSizes = { dataTypes.CLASS.value : 1, dataTypes.AMOUNT_FACES.value: 1, dataTypes.AMOUNT_VERTICES.value :1,
              dataTypes.BARY_CENTER.value : 3, dataTypes.MAX_SIZE.value : 1, dataTypes.SIZE: 1, dataTypes.DISTANCE_ORIGIN: 1}