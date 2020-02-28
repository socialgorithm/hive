from main_package.field import *
from opensimplex import OpenSimplex

class MapGenerator:
    resolution = 5
    mapScale = 30 # bigger => softer land feature
    moistureScale = 70 # bigger => softer land feature

    waterMaxElevation = 20
    sandMaxElevation = 2

    rockMinElevation = 60

    grassMinMoisture = 45
    tallGrassMinElevation = 55
    tallGrassMinMoisture = 40

    forestMinMoisture = 0
    forestMaxMoisture = 0
    forestMaxElevation = 0

    def __init__(self, width: int, height: int):
        """
        Initializes a map board of the given dimensions
        :param xdim: width (exclusive)
        :param ydim: height (exclusive)
        """
        self.width = width
        self.height = height
        self.noiseGenerator = OpenSimplex()
        self.map = self.createMap()

    def getTerrain(self, elevation: int, moisture: int) -> FieldTypeEnum:
        e = elevation * 100 # elevation [0, 100]
        m = moisture * 100  # moisture [0, 100]

        if (e < self.waterMaxElevation / 3):
            return FieldTypeEnum.DEEP_WATER
        if (e < self.waterMaxElevation):
            return FieldTypeEnum.WATER
        if (e < self.waterMaxElevation + self.sandMaxElevation):
            return FieldTypeEnum.SAND

        if (e > self.rockMinElevation):
            return FieldTypeEnum.ROCK
        if (e > self.rockMinElevation - self.sandMaxElevation):
            return FieldTypeEnum.TALL_GRASS

        if (m < self.grassMinMoisture):
            return FieldTypeEnum.DRY_GRASS
        if (e < self.forestMaxElevation and m > self.forestMinMoisture and m < self.forestMaxMoisture):
            return FieldTypeEnum.FOREST
        if (e > self.tallGrassMinElevation and m > self.tallGrassMinMoisture):
            return FieldTypeEnum.TALL_GRASS

        return FieldTypeEnum.GRASS

    def createMap(self):
        map = []

        for x in range(self.width / self.resolution):
            map[x] = []

            for y in range(self.height / self.resolution):
                elevationValue = self.getNoise(x, y, self.mapScale)
                moistureValue = self.getNoise(x, y, self.moistureScale)

                # Now use the noise values to determine the block type
                terrainType = self.getTerrain(elevationValue, moistureValue)

                map[x][y] = Field(xpos=x, ypos=y, type=terrainType)

        return map

    def getNoise(self, x: int, y: int, noiseScale: int):
        return self.noiseGenerator.noise2D(
            x = x / noiseScale,
            y = y / noiseScale
        ) / 2 + 0.5