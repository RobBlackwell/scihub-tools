# Scihub Tools

Some simple, shell-friendly tools for working with the ESA
[Sentinels Scientific Data Hub](https://scihub.copernicus.eu/)

When working at a shell prompt, you don't really want XML or JSON or
ODATA - tab delitted text is easier to play with. You want to be able
to pipe stuff between commands and redirect it to easy-to-read files.

Plus, tab delimitted text is easy to use with MS Excel, R etc.

## Installation

Requires Python 3 and the requests library which can be installed as
follows:

    pip install -r requirements.txt

## Authentication

All these commands take -u and -p flags for username and password
respectively, but you might find it easier to put your credentials in
~/.netrc instead.

Create or edit you ~/.netrc and include these lines:

    machine scihub.copernicus.eu
        login your-username
        password your-password

You might want to chmod 600 ~/.netrc for security reasons.

## scihub-search.py

You can specify your query with -q

    $ ./scihub-search.py -q "*"

For help type:

    $ ./scihub-search.py --help

To find the latest GRD data for a particular lat lon, type:

    ./scihub-search.py -q "productType:GRD AND footprint:\"Intersects(51.0, 2.0)\""

N.B. That double quotes need to be escaped in a bash shell.

This example shows the latest product ingested for the Mediterranean Sea:

    ./scihub-search.py -q "footprint:\"Intersects(POLYGON((-4.53 29.85,26.75 29.85,26.75 46.80,-4.53 46.80,-4.53 29.85)))\"&rows=1"

Without the -q argument, this script takes it's input continually from
stdin. That means you can pre-prepare queries in a file and pipe them
in. Nice and repeatable.

    cat myqueries.txt | ./scihub.py > results.txt

The output format consists of an id, a title and a summary. Here's an example:

    $ ./scihub-search.py -q "*" 
    e36ab44b-cceb-4f00-a9a7-469abb98e7af	S1A_IW_SLC__1SSH_20151122T192637_20151122T192708_008721_00C6AF_9F4D	"Date: 2015-11-22T19:26:37.617Z, Instrument: SAR-C SAR, Mode: HH, Satellite: Sentinel-1, Size: 3.92 GB"
    0f76e416-a923-4837-8fac-be1bdb6a030a	S1A_IW_SLC__1SSH_20151122T192612_20151122T192639_008721_00C6AF_63C9	"Date: 2015-11-22T19:26:12.792Z, Instrument: SAR-C SAR, Mode: HH, Satellite: Sentinel-1, Size: 3.41 GB"
    8aa5b71a-a3c2-4e2c-81e1-e22c12c6cd7a	S1A_IW_SLC__1SSH_20151122T192407_20151122T192434_008721_00C6AF_6A8B	"Date: 2015-11-22T19:24:07.693Z, Instrument: SAR-C SAR, Mode: HH, Satellite: Sentinel-1, Size: 3.41 GB"
    ..

## make-wget-script.py

Takes as input, the output described above above and creates a series
of wget commands that, when executed, will download the actual
products.

	$ ./scihub-search.py -q "*" | ./make-wget-script.py 
	wget --continue "https://scihub.esa.int/apihub/odata/v1/Products('e36ab44b-cceb-4f00-a9a7-469abb98e7af')/\$value" -O S1A_IW_SLC__1SSH_20151122T192637_20151122T192708_008721_00C6AF_9F4D.zip
	wget --continue "https://scihub.esa.int/apihub/odata/v1/Products('0f76e416-a923-4837-8fac-be1bdb6a030a')/\$value" -O S1A_IW_SLC__1SSH_20151122T192612_20151122T192639_008721_00C6AF_63C9.zip
	wget --continue "https://scihub.esa.int/apihub/odata/v1/Products('8aa5b71a-a3c2-4e2c-81e1-e22c12c6cd7a')/\$value" -O S1A_IW_SLC__1SSH_20151122T192407_20151122T192434_008721_00C6AF_6A8B.zip
	wget --continue "https://scihub.esa.int/apihub/odata/v1/Products('a6ddd7a2-2606-4e89-a2bc-dda45fdf6952')/\$value" -O S1A_IW_SLC__1SSH_20151122T192547_20151122T192614_008721_00C6AF_884E.zip
	...

## Worked Example

Let's say we want to get an image for the Isle of Wight (See example
in examples/iow)

    ../../bin/scihub-search.py -q "productType:GRD AND footprint:\"Intersects(POLYGON((-1.66 50.56, -1.04 50.56, -1.04 50.77, -1.66 50.77, -1.66 50.56)))\"&rows=1" | ../../bin/make-wget-script.py > step2.sh

Now execute step2.h to download the imagery

    ./step2.sh

We can then use GDAL to reproject the image and cut out our area of interest:

    #!/bin/sh
    export GDAL_DATA=/home/reb/anaconda3/share/gdal
    export FILE_PATH=S1A_IW_GRDH_1SDV_20160509T061446_20160509T061511_011178_010E17_D8BF.SAFE/measurement/s1a-iw-grd-vh-20160509t061446-20160509t061511-011178-010e17-002.tiff
    gdalwarp -t_srs EPSG:27700 -te_srs EPSG:4326 -r cubic -te -1.66 50.56 -1.04 50.77 $FILE_PATH iow.tiff

N.B. Many previewers might show the result as just black, in which
case you might need to hack the colour table.

    gdalinfo -mm iow.tiff

This will show you the max and min values. Say they are 35 and 2402
then you can scale the color table like this:

    gdal_translate -scale 35 2402 0 32767 iow.tiff preview.tiff

## References

https://scihub.copernicus.eu

https://scihub.copernicus.eu/userguide/5APIsAndBatchScripting

Rob Blackwell    
<rob.blackwell@cranfield.ac.uk>    
May 2016
