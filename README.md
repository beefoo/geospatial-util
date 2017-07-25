# NASA Geospatial Utilities

A collection of scripts working with geospatial data provided by NASA to generate maps that look like [NASA Earth Observations](https://neo.sci.gsfc.nasa.gov/)

## Sample workflows

### Generate custom  map

1. Identify a map that you would like to customize, e.g. [land surface temperature](https://neo.sci.gsfc.nasa.gov/view.php?datasetId=MOD11C1_E_LSTDA&year=2016)
2. Find the appropriate dataset on [the FTP site](ftp://neoftp.sci.gsfc.nasa.gov/csv/), e.g. `MOD11C1_E_LSTDA`
3. Download the appropriate .csv file, e.g. `MOD11C1_E_LSTDA_2016-01-01.CSV.gz` for January 1st, 2016
4. Run command to create a thumbnail .png:

   ```
   python csvToImg.py \
        -in data/land_surface_temperature/MOD11C1_E_LSTDA_2016-01-01.CSV.gz \
        -resize 0.2 \
        -out output/land_surface_temperature/2016-01-01.png
   ```

### Generate a composite map

```
python csvToImgComposite.py \
     -in data/land_surface_temperature/MOD11C1_E_LSTDA_2016-01-01.CSV.gz,data/sea_surface_temperature/MYD28W_2016-01-01.CSV.gz \
     -resize 0.2 \
     -out output/land_sea_surface_temperature/2016-01-01.png
```

### Batch maps

```
python batchCsvToImg.py \
     -dir data/land_surface_temperature \
     -pattern MOD11C1_E_LSTDA_([0-1\-]+).CSV.gz \
     -resize 0.2 \
     -out output/land_surface_temperature/*.png
```

### Batch composite maps

```
python batchCsvToImgComposite.py \
     -dirs data/land_surface_temperature,data/sea_surface_temperature \
     -patterns MOD11C1_E_LSTDA_([0-1\-]+).CSV.gz,MYD28W_([0-1\-]+).CSV.gz \
     -resize 0.2 \
     -out output/land_sea_surface_temperature/*.png
```
