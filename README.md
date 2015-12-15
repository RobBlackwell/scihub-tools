# Scihub Tools

Some simple, shell-friendly tools for working with the ESA
[Sentinels Scientific Data Hub](https://scihub.copernicus.eu/)

When working at a shell prompt, you don't really want XML or JSON or
ODATA - tab delitted text is easier to play with. You want to be able
to pipe stuff between commands and redirect it to easy-to-read files.

Plus, tab delimitted text is easy to use with MS Excel, R etc.

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

## Notes

Tested on a Mac. Thought to work on Linux. Might work on Windows.

## References

https://sentinel.esa.int/web/sentinel/sentinel-data-access

https://scihub.esa.int/userguide/5APIsAndBatchScripting 

Rob Blackwell <rob.blackwell@cranfield.ac.uk>
November 2015
