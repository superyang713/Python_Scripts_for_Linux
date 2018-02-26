#! /usr/bin/python3
# google.py - Use google search at the command line.
# Explanation:
#   1. Run google (with no argument) -- search the word from the clipboard.
#   2. google + words -- search the words and display the results in google.
#   3. option -t -- 'I Feel Lucky' open the webpages of the top search results.
#   4. option -t(number) -- open the specified number of webpages of the top
#      search results.


import requests
import sys
import bs4
import webbrowser
import clipboard
import re


def search(url, search_words, numOpen):
    """open specified pages of google search results"""
    res = requests.get(url + search_words)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    Search_linkElems = soup.select('h3[class="r"] a')
    for i in range(numOpen):
        webbrowser.open('http://google.com' + Search_linkElems[i].get('href'))


print('Googling...')  # display text while downloading the Google results.
url = 'http://google.com/search?q='

if len(sys.argv) == 2:
    if re.match('^-t$', sys.argv[1]):
        search_words = clipboard.paste()
        search(url, search_words, 1)
    elif re.match('^-t\d+$', sys.argv[1]):
        search_words = clipboard.paste()
        numOpen = int(sys.argv[1][2:])
        search(url, search_words, numOpen)

    if re.match('^-[^t]', sys.argv[1]):
        print('no such option is found!')

    if re.match('^[^-]', sys.argv[1]):
        search_words = sys.argv[1]
        webbrowser.open('http://google.com/search?q=' + search_words)

elif len(sys.argv) > 2:
    if re.match('^-t$', sys.argv[1]):
        search_words = ' '.join(sys.argv[2:])
        search(url, search_words, 1)
    elif re.match('^-t\d+$', sys.argv[1]):
        search_words = ' '.join(sys.argv[2:])
        numOpen = int(sys.argv[1][2:])
        search(url, search_words, numOpen)

    if re.match('^-[^t]', sys.argv[1]):
        print('no such option is found!')

    if re.match('^[^-]', sys.argv[1]):
        search_words = ' '.join(sys.argv[1:])
        webbrowser.open('http://google.com/search?q=' + search_words)

else:
    search_words = clipboard.paste()
    webbrowser.open('http://google.com/search?q=' + search_words)
