import re
import urllib.request as ur
import string
import codecs 
from timeout import timeout
from datetime import timedelta, date
import urllib.request
import zipfile


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def generate_links(start, end, template='http://data.gdeltproject.org/events/%s.export.CSV.zip'):
    """
    Generates a list of csv files to grab.
    :param start: the beginning date in the YYYY-MM-DD format (str)
    :param end: the ending date in the YYYY-MM-DD format (str)
    :returns: list of links to get
    """
    links = []
    year1, month1, day1 = start.split("-")
    year2, month2, day2 = end.split("-")                                                  

    start_dt = date(int(year1), int(month1), int(day1))
    end_dt = date(int(year2), int(month2), int(day2))

    for dt in daterange(start_dt, end_dt):
        date_string = dt.strftime("%Y%m%d")
        link = template % date_string
        links.append(link)

    return links


def grab_links(filename):
  lines = open(filename).readlines()
  links = []

  for l in lines:
    link = l.split('\t')[-1][:-1] # remove newline
    links.append(link)
	
  return links


def extract_links(link, path=''):
    zip_file = urllib.request.urlretrieve(link)
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(path)
    zip_ref.close()
    file_name = link.split('/')[-1]
    file_name = file_name[:file_name.indexof('.zip')]
    file_name = path + '/' + file_name
    print(zip_name)	


def clean_text(text):
  cleantext = codecs.getdecoder("unicode_escape")(text)

  # clean html
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', cleantext)

  # clean braket
  cleanr = re.compile('{.*?}')
  cleantext = re.sub(cleanr, ' ', cleantext)

  cleantext = ' '.join(cleantext.split('\n'))
  return cleantext


@timeout(3)
def get_text(link, outfile=None):
  try:
    page = ur.urlopen(link)
    return str(page.read()) 
  except:
    return ''
