
import rasterio
import rasterio.features
import rasterio.warp


def convertPixelPlacementToCoordinates(fileName, point):
    with rasterio.open(fileName) as dataset:

        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):

            (x, y) = point

            pointx, pointy = dataset.xy(x, y)

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).

            xarr = []
            yarr = []
            for v in geom['coordinates'][0]:
                xarr.append(v[0])
                yarr.append(v[1])

            ds = rasterio.warp.transform(
                'EPSG:5972', 'EPSG:4326', [pointx], [pointy])

            geom = rasterio.warp.transform_geom(
                'EPSG:5972', 'EPSG:4326', geom, precision=6)

            return (ds[1][0], ds[0][0])
