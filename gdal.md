# List of GDAL commands

Show file information:

```
gdalinfo geotiff/water_vapor_m/MYDAL2_M_SKY_WV_2016-01.FLOAT.TIFF
```

Convert a GeoTIFF to ASCII grid

```
gdal_translate -of AAIGrid geotiff/water_vapor_m/MYDAL2_M_SKY_WV_2016-01.FLOAT.TIFF geotiff/water_vapor_m/MYDAL2_M_SKY_WV_2016-01.asc
```
