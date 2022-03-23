

from fileinput import filename
import tifffile
import rasterio
import rasterio.features
import rasterio.warp

from PIL import Image

fileName = 'assets/tif-examples/02_raster/007.tif'
# image = Image.open(fileName)
# print(dir(image))
# print(image.info)


# ds = gdal.Open(fileName, gdal.GA_ReadOnly)
# rb = ds.GetRasterBand(1)
# img_array = rb.ReadAsArray()


# with tifffile.TiffFile(fileName) as tif:
#     tif_tags = {}
#     for tag in tif.pages[0].tags.values():
#         name, value = tag.name, tag.value
#         tif_tags[name] = value
#     print(tif_tags)
#     image = tif.pages[0].asarray()

debugRaster = True

if debugRaster:

    with rasterio.open(fileName) as dataset:

        print(dir((dataset.crs)))
        print(dataset.crs.to_string())
        print(dataset.crs)

        # Read the dataset's valid data mask as a ndarray.
        mask = dataset.dataset_mask()

        print(dataset.transform)
        # Extract feature shapes and values from the array.
        for geom, val in rasterio.features.shapes(
                mask, transform=dataset.transform):

            print(val)
            print(geom)

            print(dataset.xy(2500, 2500))

            # Transform shapes from the dataset's own coordinate
            # reference system to CRS84 (EPSG:4326).
            geom = rasterio.warp.transform_geom(
                'EPSG:5972', 'EPSG:4326', geom, precision=6)

            # Print GeoJSON shapes to stdout.
            print(geom)
