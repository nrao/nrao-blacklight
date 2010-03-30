import csv
import datetime
import pytz
import sys
import user

def get_utc_datetime(timestamp, format='%Y-%m-%dT%H:%M:%S', tz='US/Eastern'):
    timezone = pytz.timezone(tz)
    utc = pytz.utc
    try:
        dt = datetime.datetime.strptime(timestamp, format)
    except ValueError:
        return None
    if dt.year < 1900:
        return None
    return timezone.localize(dt).astimezone(utc)

def utc_datetime(record):
    return get_utc_datetime(record.get('DATE-OBS', ''), tz='UTC')

def velocity(record):
    # m/s to km/s
    given = record.get('VELOCITY')
    if (given is None or given == ''):
        return None
    else:
        return float(given) / 1000.0

def skyfreq(record):
    # Hz to GHz
    given = record.get('SKYFREQ')
    if (given is None or given == ''):
        return None
    else:
        return float(given) / 1000000000.0

def doc_it(record):
    if record.get('PROJID') and record.get('SCAN'):
        doc_id = record.get('PROJID') + '-' + record.get('SCAN')
    else:
        # ID is required.
        doc_id = None
        return {}
    items = [('id', doc_id),
             ('session', record.get('PROJID')),
             ('object', record.get('OBJECT')),
             ('observer', record.get('OBSERVER')),
             ('datetime', utc_datetime(record)),
             ('procname', record.get('PROCNAME')),
             ('velocity', velocity(record)),
             ('veldef', record.get('VELDEF')),
             ('skyfreq', skyfreq(record)),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ]
    return dict([(k, v) for k, v in items if (v is not None and v != '')])

docs = (doc_it(record) for record in csv.DictReader(open('data.csv')))
