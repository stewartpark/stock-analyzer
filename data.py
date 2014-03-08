import datetime
import urllib2
import StringIO
import csv
from dateutil import parser as dateparser
import base64
import os.path 
import tempfile
import pickle 

def totimestamp(t):
    epoch = datetime.datetime(1970, 1, 1)
    diff = t-epoch
    return diff.days * 24 * 3600 + diff.seconds

def load_data(id):
    """
        Download historical prices of a certain resource with ID via Quandl.

        Market indices, stock, currency, commodities.

        (the auth token is jyp's. please do not use it.)
    """
    now = datetime.datetime.now() 
    tmpn = os.path.join(tempfile.gettempdir(), base64.b64encode(str(now.day) + id))
    if not os.path.exists(tmpn):
        url = "http://www.quandl.com/api/v1/datasets/%s.csv?&trim_start=%04d-01-01&trim_end=%04d-%02d-%02d&sort_order=asc&auth_token=7iwuPnR7yrS1uoQszmjB" % (id, now.year-10,now.year, now.month, now.day)

        res = urllib2.urlopen(url)
        f = StringIO.StringIO(res.read())
        reader = csv.reader(f)
        data=[]
        reader.next()
        for row in reader:
            try:
                t = dateparser.parse(row[0])
                data.append([ totimestamp(t), float(row[1]) ])
            except:
                pass
        pickle.dump(data, open(tmpn, 'w'))
    else:
        data = pickle.load(open(tmpn)) 
    return data
    
if __name__ == '__main__':
    # Example
    print load_data('GOOG/NYSE_CVX')
