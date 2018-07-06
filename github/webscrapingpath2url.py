# This is the "official" translating module I wrote for my translator
# To use: import webscraping as ws
# ws.transmodule(transtextinput, sl, tl)
# sl and tl are saved in a txt file as option which I will deal with next week
import mechanize
import urllib

def transmodule(transtextinput, tl, sl = 'auto'):
    translated = translate(transtextinput, tl, sl)
    return translated.replace('\\n', '').decode('utf-8')

def translate(transtextinput, tl, sl):
    # input the text for translation
    # convert " " into "%20", "\n" into "%0A", etc.
    transtext = urllib.pathname2url(transtextinput)
##    print """Please use the following abbreviation for the languages: \
##en-English, zh-CN-Chinese (simplified), es-Spanish, de-German, fr-French, \
##auto-Autodetect"""

    url = ("https://translate.googleapis.com/translate_a/single?client=gtx&sl="
           + sl + "&tl=" + tl + "&dt=t&q=" + transtext)
##    print url
    browser = mechanize.Browser()
    browser.set_handle_robots(False)# ignore robots.txt (anti-crawler)
    # I have mechanize browser claim to be Chrome (google demands a non-robot
    # user-agent I guess) since I grab the url using Chrome, I didn't try
    # another browser so I just set it to be Chrome
    browser.addheaders = [("User-agent", "Chrome")]

    fin = browser.open(url)
    content = fin.read()
    print '================'
    print content
    start = 4 # webscraping string always starts with [[["
    end = content.index('"', start)
    result = content[start:end]
    print result
    for line in xrange(transtextinput.count('\n')):
        # overwrite the start with the start of the new line
        start = content.index('["', end) + 2
        end = content.index('"', start)
        result = result + '\n' + content[start:end]
    result.replace('\\n', '')
    return result