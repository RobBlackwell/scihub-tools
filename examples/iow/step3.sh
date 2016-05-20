#!/bin/sh
export GDAL_DATA=/home/reb/anaconda3/share/gdal
export FILE_PATH=S1A_IW_GRDH_1SDV_20160509T061446_20160509T061511_011178_010E17_D8BF.SAFE/measurement/s1a-iw-grd-vh-20160509t061446-20160509t061511-011178-010e17-002.tiff
gdalwarp -t_srs EPSG:27700 -te_srs EPSG:4326 -r cubic -te -1.66 50.56 -1.04 50.77 $FILE_PATH iow.tiff
