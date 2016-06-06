#!/usr/bin/env python

import sys
from optparse import OptionParser

# You might consider putting your scihub credentials in ~/.netrc

def curl_command (username, password, uuid, title):
    user_option = ''

    if username is not None:
        user_option = ' -u {}:{}'.format(username,password)

    s = 'curl {} --retry 5 -C - -n "https://scihub.copernicus.eu/apihub/odata/v1/Products(\'{}\')/\$value" -o {}.zip'.format(user_option, uuid, title)
    return s


def toploop(username, password):

    filename = None
    while 1:
        uuid = sys.stdin.readline()
        if not uuid: break
        x = uuid.split()
        if len(x) > 1:
            uuid = x[0]
            title = x[1]
            print (uuid)
            print(title)
            print(curl_command (username, password, uuid, title))


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user',
                      help='Your Scihub username.')
    parser.add_option('-p', '--password', dest='password',
                      help='Your Scihub password.')
    parser.add_option( '--uuid', dest='uuid',
                       help='UUID of a scihub product.')
    parser.add_option( '--title', dest='title',
                       help='Title of a scihub product.')

    (options, args) = parser.parse_args()

    username = options.user
    password = options.password
    uuid = options.uuid
    title = options.title

    if uuid is None:
        toploop(username, password)
    else:
        print(curl_command(username, password, uuid, title))
