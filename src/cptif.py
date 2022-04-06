
import rasterio
from rasterio.transform import from_origin


inputData = None

inName = 'assets/tif-examples/02_raster/007.tif'
outName = 'assets/tif-examples/02_raster/007-cp.tif'


with rasterio.open(inName, "r") as ip:
    # print(ip)

    # print(dir(ip))
    inputData = ip

    print(ip.meta)

    # with rasterio.open('example.tif',
    #                    'w',
    #                    driver='GTiff',
    #                    dtype='uint16',
    #                    width=720,
    #                    height=360,
    #                    count=8,
    #                    crs='EPSG:4326',
    #                    transform=from_origin(-180.0, 90.0, 0.5, 0.5),
    #                    nodata=0,
    #                    tiled=True,
    #                    compress='lzw') as dataset:

    #     dataset.write("test.tif")
