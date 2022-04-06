import tiffile
from PIL import Image
import rasterio
import json


inName = 'assets/tif-examples/02_raster/007.tif'
mockedTif = "assets/tif-examples/02_raster/mock_007_png.png"
outName = 'assets/tif-examples/02_raster/007-cp.tif'

image = Image.open(mockedTif)

imPil = Image.open(inName)

image.save("output.tif", "TIFF", exif=imPil.getexif().tobytes())

im = tiffile.imread(inName)

exif = imPil.getexif()
metaD = json.dumps(str(exif))

print(metaD)
print(exif.tobytes())

# print(dir(im))

with rasterio.open(inName, "r") as f:
    # print(f.meta)
    # jsonedData = json.dumps(f.meta)
    # metadata=json.loads(metaD))
    # tiffile.imwrite("output.tif", data=image,
    #                 metadata = {'filename': 'styrkern'})
    pass
