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

def price_is_right(bands, freq):
    "Return the closest band in bands without going over target."
    freq_band = None
    if freq is None or not bands:
        return None
    for band_key in sorted(bands.keys()):
        if band_key > freq:
            break
        freq_band = bands[band_key]
    return freq_band

bands = {0.0: '4-band',
         0.225: 'P-band',
         0.390: '450-band',
         0.510: '600-band',
         0.680: '800-band',
         1.0: 'L-band',
         2.0: 'S-band',
         4.0: 'C-band',
         8.0: 'X-band',
         12.0: 'Ku-band',
         18.0: 'K-band',
         26.5: 'Ka-band',
         40.0: 'Q-band',
         50.0: 'V-band',
         75.0: 'W-band',
         }

def band(record):
    """Create a band parameter given a record with skyfreq.

    From Dana, 2010-03-30:
    4-band:   near 74 MHz
    P-band:   0.225 -   0.390 GHz
    450-band: 0.390 -   0.510 GHz
    600-band: 0.510 -   0.680 GHz
    800-band: 0.680 -   1.0   GHz
    L-band:   1.0   -   2.0   GHz
    S-band:   2.0   -   4.0   GHz
    C-band    4.0   -   8.0   GHz
    X-band:   8.0   -  12.0   GHz
    Ku-band: 12.0   -  18.0   GHz (sometimes called U)
    K-band:  18.0   -  26.5   GHz
    Ka-band: 26.5   -  40.0   GHz
    Q-band:  40.0   -  50.0   GHz
    V-band:  50.0   -  75.0   GHz (typically not used due to O2 line)
    W-band:  75.0   - 110.0   GHz 
    """
    return price_is_right(bands, skyfreq(record))

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
             ('band', band(record)),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ('', record.get('')),
             ]
    return dict([(k, v) for k, v in items if (v is not None and v != '')])

docs = (doc_it(record) for record in csv.DictReader(open('data.csv')))
