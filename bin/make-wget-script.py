#!/usr/bin/env python

import sys
from optparse import OptionParser

# You might consider putting your scihub credentials in ~/.netrc
    
def wget_command (username, password, uuid, filename):
    user_option = ''
    password_option = ''
    filename_option = ''
    
    if filename is not None:
        filename_option = ' -O {}.zip'.format(filename)
        
    if username is not None:
        user_option = ' -user={}'.format(username)

    if password is not None:
        password_option = ' --passwrod={}'.format(password)
        
    s = 'wget --continue{}{} "https://scihub.copernicus.eu/apihub/odata/v1/Products(\'{}\')/\$value"{}'.format(user_option, password_option, uuid, filename_option)

    print s


            
def toploop(username, password):

    filename = None
    while 1:
        uuid = sys.stdin.readline()
        if not uuid: break
        x = uuid.split()
        if len(x) > 0:
            uuid = x[0]
        if len(x) > 1:
            filename = x[1]
        wget_command (username, password, uuid, filename)
    

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option('-u', '--user', dest='user',
                      help='Your Scihub username.')
    parser.add_option('-p', '--password', dest='password',
                      help='Your Scihub password.')
    parser.add_option( '--uuid', dest='uuid',
                      help='UUID of a scihub product.')
    parser.add_option('-O', '--output', dest='output',
                      help='Output filename.')
      
    (options, args) = parser.parse_args()

    username = options.user
    password = options.password
    uuid = options.uuid
    filename = options.output

    if uuid is None:
        toploop(username, password)
    else:
        wget_command(username, password, uuid, filename)

