import csv
from HTMLParser import HTMLParser
import re
import urllib2
import time

#Uses BeautifulSoup 3, the syntax has since changed,
#so this may need to be updated
from BeautifulSoup import BeautifulSoup as bs

class BirdGatherer:
    def __init__(self, max_tries=10, sleep_dur=3):
        ''' Set up our bird BirdGatherer with basic params '''
        self.max_tries = max_tries
        self.base_url = 'http://nzbirdsonline.org.nz'
        self.search_url = '{}/name-search?field_other_names_value=&title=&page='.format(self.base_url)
        self.bird_counter = 0
        self.sleep_dur = sleep_dur # if an attempt fails, sleep a few seconds

    def count_results_pages(self):
        ''' Find the number of results pages '''
        soup = bs(urllib2.urlopen(self.search_url).read())
        self.num_results_pages = int(
            re.match('.*page=(?P<page>\d+)',
            soup.find('li', 'pager-last').find('a').attrs[1][1]).groups()[0]
        )
        print('There are {} pages of results.'.format(self.num_results_pages))

    def gather_birds(self, dst_file='nzbirdsonline_index.csv'):
        ''' Loop through result pages and extract data for each bird '''
        # figure out how many pages there are
        self.count_results_pages()

        # open CSV for writing
        with open(dst_file, 'w') as output:
            birds_csv = csv.writer(output)
            # write the header
            birds_csv.writerow([
                'common_name',
                'order',
                'family',
                'scientific_name',
                'conservation_status', # this was status in earlier version
                'nz_status',
                'url'
            ])

            for page in range(self.num_results_pages + 1):
                # construct the search URL
                url = '{}{}'.format(self.search_url, page)
                # reset attempt counter
                tries = 0
                while tries < self.max_tries:
                    print('Attempt {} retrieving: {}'.format(tries, url))
                    try:
                        # parse the page and break if successful
                        soup = bs(urllib2.urlopen(url).read())
                        tries = self.max_tries
                        break
                    except urllib2.URLError:
                        # sleep briefly if there's an error
                        tries += 1
                        time.sleep(self.sleep_dur)

                # parse the page results, getting structured page data back in a list
                page_results = self.parse_result_page(page, soup)
                # write each item in list to csv
                for result in page_results:
                    birds_csv.writerow(result)
                print('---\n')

    def get_infobox_text(self, label, detail):
        ''' Extract data from detail page info-box '''
        try:
            return detail(text=label)[0].parent.parent.find('a').contents[0]
        except IndexError:
            return ''

    def parse_result_page(self, page, soup):
        ''' Parse each bird on the result page '''
        results = []
        for result in soup.findAll('div', 'search-result-text'):
            self.bird_counter += 1

            # extract data from the results page
            name = HTMLParser().unescape(result.find('h3', 'search-result-title').find('a')\
                .contents[0]).encode('ascii', 'replace')
            name = name.replace("Stirton?s", "Stirton's") # TODO - make more robust

            url = self.base_url + result.find('h3', 'search-result-title').find('a')\
                .attrs[0][1].encode('ascii', 'replace')

            scientific = HTMLParser().unescape(result.find('p', 'search-result-scientific').\
                contents[0]).encode('ascii', 'replace')

            con_status = result.find('p', 'search-result-status').contents[1].encode('ascii', 'replace')
            tries = 0

             # Get detail page for each bird
            while tries < self.max_tries:
                try:
                    print('  Getting details for "{}" (attempt {}) {}'.format(name, tries, url))
                    detail = bs(urllib2.urlopen(url).read())
                    tries = self.max_tries
                    break
                except urllib2.URLError:
                    # sleep briefly if there's an error
                    tries += 1
                    time.sleep(self.sleep_dur)

            # extract additional data from details page
            order       = self.get_infobox_text('Order: ', detail)
            family      = self.get_infobox_text('Family: ', detail)
            nz_status   = self.get_infobox_text('New Zealand status: ', detail)

            # compile results into a single line for export to CSV
            results.append([
                name.strip(),
                order.strip(),
                family.strip(),
                scientific.strip(),
                con_status.strip(),
                nz_status.strip(),
                url.strip()
            ])
            print('  Got {} ({})'.format(name, self.bird_counter))
        return results


def main():
    bg = BirdGatherer()
    bg.gather_birds(dst_file='nzbirdsonline_index.csv')

if __name__ == '__main__':
    main()
