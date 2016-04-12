import csv
from HTMLParser import HTMLParser
import re
import urllib2

#Uses BeautifulSoup 3, the syntax has since changed,
#so this may need to be updated
from BeautifulSoup import BeautifulSoup as bs

nzbirds_base = 'http://nzbirdsonline.org.nz'
nzbirds_first = nzbirds_base + \
    '/name-search?field_other_names_value=&title='
nzbirds_page = nzbirds_first+'&page=%i'

#Find the number of pages
soup = bs(urllib2.urlopen(nzbirds_first).read())
pages = int(re.match('.*page=(?P<page>\d+)', 
    soup.find('li', 'pager-last').find('a').attrs[1][1]).groups()[0])
print '%s pages'%pages

#Now parse each page
count = 0

with open('nzbirdsonline_index.csv', 'w') as output:
    birds = csv.writer(output)
    birds.writerow(('common_name', 'scientific_name', 'status', 'url'))
    for page in range(pages + 1):
        soup = bs(urllib2.urlopen(nzbirds_page % page).read())
        for result in soup.findAll('div', 'search-result-text'):
            count += 1
            name = HTMLParser().unescape(result.find('h3', 
                'search-result-title').find('a').contents[0]).encode('ascii', 'replace')
            name = name.replace("Stirton?s", "Stirton's")
            url = nzbirds_base + result.find('h3', 
                'search-result-title').find('a').attrs[0][1].encode('ascii', 'replace')
            scientific = HTMLParser().unescape(result.find('p', 
                'search-result-scientific').contents[0]).encode('ascii', 'replace')
            status = result.find('p', 'search-result-status').contents[1].encode('ascii', 'replace')
            birds.writerow((name.strip(), scientific.strip(), status.strip(), url.strip()))
        print 'Page %s, %s birds' % (page, count)

