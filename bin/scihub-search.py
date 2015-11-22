#!/usr/bin/env python

import sys
import requests
import getpass
import json
from optparse import OptionParser

# Runs Open search queries against the Sentinels Scientific Data Hub.
# You might consider putting tour credentials in ~/.netrc
# Output is tab delimitted text of the format
# id filename description

def print_entry(entry):
    id =  entry['id']
    title =  entry['title']
    summary =  entry['summary']
    print '{}\t{}\t"{}"'.format(id, title, summary)
    
def search (auth, query):

    url = 'https://scihub.esa.int/apihub/search?format=json&q={}'.format(query)

    #print url
    #exit()
    
    response = requests.get(url, auth=auth)

    #print response.status_code
    #print response.text
    #exit()

    if response.status_code == 200:
        j = json.loads(response.text)

        entries = j['feed']['entry']

        # An entry can be a single entry or a list of entries.
        if isinstance(entries, list):
            for entry in entries:
                print_entry(entry)
        else:
            print_entry(entries)
            
def toploop(auth):

    while 1:
        query = sys.stdin.readline()
        if not query: break
        x = query.split()
        if len(x) > 0:
            query = x[0]
        search (auth, query)
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user',
                      help='Your Scihub username.')
    parser.add_option('-p', '--password', dest='password',
                      help='Your Scihub password.')
    parser.add_option('-q', '--query', dest='query',
                      help='Open search query expression.')
      
    (options, args) = parser.parse_args()

    username = options.user
    password = options.password

    if username is not None:
            if password is  None:
                password = getpass.getpass()
            auth = (username, password)
    else:
        # No auth falls back to ~/.netrc
        auth = None

    query = options.query

    if query is None:
        toploop(auth)
    else:
        search(auth, query)

