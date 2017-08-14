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

This will make a composite of the land surface and sea surface temperature data

```
python csvToImgComposite.py \
     -in data/land_surface_temperature/MOD11C1_E_LSTDA_2016-01-01.CSV.gz,data/sea_surface_temperature/MYD28W_2016-01-01.CSV.gz \
     -resize 0.2 \
     -out output/land_sea_surface_temperature/2016-01-01.png
```

### Batch maps

This will create frames for all land surface temperature files in directory

```
python batchCsvToImg.py \
     -dir data/land_surface_temperature \
     -pattern MOD11C1_E_LSTDA_([0-1\-]+).CSV.gz \
     -resize 0.2 \
     -out output/land_surface_temperature/*.png
```

### Batch composite maps

This will create frames for all land surface temperature files in directory

```
python batchCsvToImgComposite.py \
     -dirs data/land_surface_temperature,data/sea_surface_temperature \
     -patterns MOD11C1_E_LSTDA_([0-1\-]+).CSV.gz,MYD28W_([0-1\-]+).CSV.gz \
     -resize 0.2 \
     -out output/land_sea_surface_temperature/*.png
```

### Execute batch based on instructions file

```
python batchInstructionsToImg.py \
      -in data/instructions.json
      -keys land_sea_surface_temperature,vegetation_index
```

### Convert a set of frames to a movie using interpolation

First, create a movie file with [ffmpeg](https://www.ffmpeg.org/)

```
ffmpeg -framerate 30/1 -i output/land_sea_surface_temperature/frame%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p -q:v 1 output/land_sea_surface_temperature_30fps.mp4
```

Set a new duration (60s) with interpolation using [butterflow](https://github.com/dthpham/butterflow) (can take a long time!)

```
butterflow -s a=0,b=end,dur=60 output/land_sea_surface_temperature_30fps.mp4
```
