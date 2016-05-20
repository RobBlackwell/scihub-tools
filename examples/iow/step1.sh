#!/bin/sh
../../bin/scihub-search.py -q "productType:GRD AND footprint:\"Intersects(POLYGON((-1.66 50.56, -1.04 50.56, -1.04 50.77, -1.66 50.77, -1.66 50.56)))\"&rows=1" | ../../bin/make-wget-script.py > step2.sh


