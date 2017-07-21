# MODIS Utilities

A collection of scripts working with geospatial data provided by [MODIS](https://modis.gsfc.nasa.gov/) to generate maps that look like [NASA Earth Observations](https://neo.sci.gsfc.nasa.gov/)

## Sample workflows

### Generate custom  map

1. Identify a map that you would like to customize, e.g. [land surface temperature](https://neo.sci.gsfc.nasa.gov/view.php?datasetId=MOD11C1_E_LSTDA&year=2016)
2. Find [dataset](https://modis.gsfc.nasa.gov/data/dataprod/mod11.php) on [MODIS](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table) website, e.g. [MOD11C2](https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod11c2) for 8-day, 0.05-deg resolution
3. Download the appropriate .hdf file, e.g. [MOD11C2.A2016001.006.2016234032340.hdf](https://e4ftl01.cr.usgs.gov/MOLT/MOD11C2.006/2016.01.01/) for January 1st, 2016
4. Run `python h4toh5.py` to convert .hdf to .h5
5. Inspect file: `python h5.py -in data/land_surface_temperature/MOD11C2.A2016001.006.2016234032340.h5`
5. Run command to create a .png:
   ```
   python h5ToImg.py \
        -in data/land_surface_temperature/MOD11C2.A2016001.006.2016234032340.h5 \
        -dataset "MODIS_8DAY_0.05DEG_CMG_LST,Data Fields,LST_Day_CMG" \
        -resize 0.2 \
        -out output/land_surface_temperature/20160101.png
   ```
