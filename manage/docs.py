"""Provide an iterator of Solr docs of scans in the GBT archive.

Currently works from a CSV dump of all scans in the GBT archive.
See project gbt-fits-dump, which is run on bigdog.cv.nrao.edu.
"""

import csv
import datetime
import sys
import user

import pytz

def proposal_id(record):
    """Get a proposal_id value given a scan dict record."""
    if record.has_key('proposal_id'):
        return record['proposal_id']
    given = record.get('PROJID')
    if (given is None or given == ''):
        return None
    pass
    prop_id = None
    record['proposal_id'] = prop_id
    return None

def legacy_id(prop_id):
    """Get a legacy_id value given a proposal ID."""
    pass
    return None

def session_id(record):
    """Get session ID (based on proposal ID) value given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def title(record):
    """Get the project title (proposal) given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def abstract(record):
    """Get the project abstract (proposal) given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def pi(record):
    """Get the project PI (proposal) given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def investigators(record):
    """Get the project investigators (proposal) given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def get_utc_datetime(timestamp, format='%Y-%m-%dT%H:%M:%S', tz='US/Eastern'):
    """Get a UTC datetime object given a timestamp string."""
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
    """Get a UTC datetime value given a scan dict record."""
    return get_utc_datetime(record.get('DATE-OBS', ''), tz='UTC')

def velocity(record):
    """Get a velocity value given a scan dict record, convert m/s to km/s."""
    given = record.get('VELOCITY')
    if (given is None or given == ''):
        return None
    else:
        return float(given) / 1000.0

def skyfreq(record):
    """Get a skyfreq value given a scan dict record, convert Hz to GHz."""
    given = record.get('SKYFREQ')
    if (given is None or given == ''):
        return None
    else:
        return float(given) / 1000000000.0

def price_is_right(bands, freq):
    """Return the closest band in bands without going over freq."""
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
    """Get (create) a band value given a scan dict record.

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

def restfreq(record):
    """Get restfreq values given a scan dict record, convert MHz to GHz."""
    given = record.get('config_restfreq')
    if (given is None or given == ''):
        return None
    else:
        restfreqs = given.split(',')
        return [float(f) / 1000.0 for f in restfreqs]

def ra_dec(record):
    """Get a ra, dec value pair given a scan dict record."""
    loc = record.get('config_restfreq')
    if (loc is None or loc == ''):
        return None, None
    pass
    return None, None

def bandwidth(record):
    """Get a bandwidth value given a scan dict record."""
    given = record.get('config_bandwidth')
    if (given is None or given == ''):
        return None
    return float(given)

def doc_it(record):
    """Create a Solr doc (dict for pysolr) given a scan dict record."""
    if record.get('PROJID') and record.get('SCAN'):
        doc_id = record.get('PROJID') + '-' + record.get('SCAN')
    else:
        # ID is required.
        doc_id = None
        return {}
    ra, dec = ra_dec(record)
    items = [('id', doc_id),
             ('tel', 'GBT'),
             ('proposal_id', proposal_id(record)),
             ('legacy_id', legacy_id(record)),
             ('session_id', session_id(record)),
             ('title', title(record)),
             ('abstract', abstract(record)),
             ('pi', pi(record)),
             ('investigators', investigators(record)),
             ('projid', record.get('PROJID')),
             ('session', record.get('PROJID')),
             ('object', record.get('OBJECT')),
             ('observer', record.get('OBSERVER')),
             ('date-obs', utc_datetime(record)),
             ('procname', record.get('PROCNAME')),
             ('velocity', velocity(record)),
             ('obstype', record.get('OBSTYPE')),
             ('veldef', record.get('VELDEF')),
             ('skyfreq', skyfreq(record)),
             ('band', band(record)),
             ('restfreq', restfreq(record)),
             ('ra', ra),
             ('dec', dec),
             ('pol', record.get('config_pol')),
             ('receiver', record.get('config_receiver')),
             ('bandwidth', bandwidth(record)),
             ]
    return dict([(k, v) for k, v in items if (v is not None and v != '')])

# Create generator for lazy iteration over all scans in CSV dump of GBT data.
docs = (doc_it(record) for record in csv.DictReader(open('data.csv')))
