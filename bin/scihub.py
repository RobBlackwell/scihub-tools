#!/usr/bin/env python
import requests
import json

# Runs Open search queries against the Sentinels Scientific Data Hub.

def raw_search (query, auth=None):

    # auth = None falls back to using credentials from ~.netrc
    url = 'https://scihub.copernicus.eu/apihub/search?format=json&q={}'.format(query)

    response = requests.get(url, auth=auth)

    #print(response.status_code)
    #print(response.text)
    #exit()

    if response.status_code == 200:
        return response.text
    else:
        raise ValueError('Query failed : %s:%s\n' % (response.status_code, response.text))


def search (query, auth=None):

    s = raw_search(query, auth)
    j = json.loads(s)

    # print(j)
    entries = None
    if 'entry' in j['feed']:
        entries = j['feed']['entry']

    #print(entries)
    return entries


def summary(entry):
    return { 'id' : entry['id'],
             'title' : entry['title'],
             'summary' : entry['summary']}

def filename(entry):
    return '{}.zip'.format(entry['title'])

def curl_command(entry):
    url = entry['link'][0]['href'].replace("$","\$")
    f = filename(entry)
    s = 'curl --retry 5 -C - -n "{}" -o {}'.format(url, f)
    return(s)


def unzip_command(entry):
    f = filename(entry)
    s = "unzip {0}".format(f)
    return (s)
