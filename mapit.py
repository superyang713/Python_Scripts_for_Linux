#! /usr/bin/python3
# mapit.py - launches a map in the broweser using an address from
# the command line or clipboard


import webbrowser, sys, clipboard

if len(sys.argv) > 1:
    # Get address from command line.
    address = ' '.join(sys.argv[1:])
else:
    # Get address from clipboard.
    address = clipboard.paste()

webbrowser.open('https:www.google.com/maps/place/' + address)
