import csv
import datetime
import pytz
import sys
import user

if '-m' in sys.argv:
    i = sys.argv.index('-m')
    name = sys.argv[i+1]
    print 'using module named', name
    module = __import__(name)
    raw_docs = module.docs
else:
    raw_docs = [record for record in csv.DictReader(open('data.csv'),
                                                    delimiter=',')]

docs = []

def get_utc_datetime(timestamp, format='%Y-%m-%d %H:%M:%S', tz='US/Eastern'):
    timezone = pytz.timezone(tz)
    utc = pytz.utc
    dt = datetime.datetime.strptime(timestamp, format)
    return timezone.localize(dt).astimezone(utc)

multifields = ('source', 'observer', 'starttime', 'frequency', 'detector',
               'receiver', 'band', 'polarization', 'year', 'month',)

display_exceptions = ('source', 'starttime', 'frequency', 'year', 'month',)

display_fields = tuple([k for k in multifields if k not in display_exceptions])

# This can be simplified, but let's make it work first.
for raw_doc in raw_docs:
    doc = dict()
    for k,v in raw_doc.items():
        v = v or ''
        # v = v.decode('utf8')
        if k in multifields:
            doc[k] = v.split(':::')
        else:
            doc[k] = v
    doc['id'] = doc.get('project_session', '')
    for key in display_fields:
        doc[key + '_display'] = ', '.join(doc[key])
    doc['frequency_display'] = '\n'.join(doc['frequency'])
    doc['source_display'] = '\n'.join(doc['source'])

    starttimes = doc.get('starttime', [])
    formatted_starttimes = []
    for starttime in starttimes:
        try:
            formatted_starttimes.append(get_utc_datetime(starttime, tz='UTC'))
        except ValueError:
            pass
    if formatted_starttimes:
        doc['starttime'] = formatted_starttimes
    else:
        doc.pop('starttime', None)

    if doc.get('lastdate', ''):
        doc['lastdate'] = get_utc_datetime(doc['lastdate'], tz='UTC')
    doc['frequency'] = [int(x) for x in doc['frequency']]
    doc['year'] = [int(x) for x in doc['year']]
    doc['month'] = [int(x) for x in doc['month']]

    [doc.pop(k) for k,v in doc.items() if not v]

    if doc.get('id', ''):
        docs.append(doc)
