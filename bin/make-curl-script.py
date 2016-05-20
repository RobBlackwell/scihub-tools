#!/usr/bin/env python

import sys
from optparse import OptionParser

# You might consider putting your scihub credentials in ~/.netrc

def curl_command (username, password, uuid):
    user_option = ''

    if username is not None:
        user_option = ' -u {}:{}'.format(username,password)

    s = 'curl --retry 5 -C - -n -JO{} "https://scihub.copernicus.eu/apihub/odata/v1/Products(\'{}\')/\$value"'.format(user_option,uuid)

    print (s)


def toploop(username, password):

    filename = None
    while 1:
        uuid = sys.stdin.readline()
        if not uuid: break
        x = uuid.split()
        if len(x) > 0:
            uuid = x[0]
        curl_command (username, password, uuid)


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user',
                      help='Your Scihub username.')
    parser.add_option('-p', '--password', dest='password',
                      help='Your Scihub password.')
    parser.add_option( '--uuid', dest='uuid',
                      help='UUID of a scihub product.')

    (options, args) = parser.parse_args()

    username = options.user
    password = options.password
    uuid = options.uuid

    if uuid is None:
        toploop(username, password)
    else:
        curl_command(username, password, uuid)
