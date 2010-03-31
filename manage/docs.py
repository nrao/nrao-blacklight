"""Provide an iterator of Solr docs of scans in the GBT archive.

Currently works from a CSV dump of all scans in the GBT archive.
See project gbt-fits-dump, which is run on bigdog.cv.nrao.edu.
"""

import csv
import datetime
import re
import sys
import user

import pytz

import proposal

def is_a_value(x):
    return (x is not None and x != '' and x != [])

# We are dealing with several cases of project names in the archive.
# Example 1: AGBT10A_001, GBT10A_001, AGBT_05B_046
idcase1 = re.compile('^A?GBT[-|_]*(\d{2}[ABC])[-|_]*(\d{2,3})', re.I)
# Example 2: ABB240, BB240
idcase2 = re.compile('^A?B([A-Z])0*(\d{2,3})', re.I)
# Example 3: AGH009, GH009, AGV020, GV020
idcase3 = re.compile('^A?G([A-Z])0*(\d{2,3})', re.I)
# Example 4: AGLST011217, GLST011217
idcase4 = re.compile('^A?GLST0*(\d{4,5})', re.I)

def fetch_ids(record):
    """Fetch/determine essential IDs given a scan dict record.

    Given complexity in dealing with IDs, this function has some side effects:
     * store proposal ID to record['proposal_id']
     * store legacy ID to record['legacy_id']
     * store base for document ID to record['base_id']
     * store some alternate IDs to record['alt_ids']
     * store a flag indicating fetched_ids to record['fetched_ids']

    There are several cases where document ID should be based on the legacy ID.
    As such, the logic is currently encoded up front in determining the IDs.
    """
    if record.has_key('fetched_ids'):
        return
    given = record.get('PROJID')
    if not is_a_value(given):
        record['fetched_ids'] = True
        return
    match1 = idcase1.search(given)
    match2 = idcase2.search(given)
    match3 = idcase3.search(given)
    match4 = idcase4.search(given)
    prop_id = None
    leg_id = None
    base_id = None
    alt_ids = []
    if match1:
        trimester, num = match1.groups()
        if len(num) < 3:
            num = '0' + num
        prop_id = 'GBT/%s-%s' % (trimester, num)
        base_id = prop_id
    elif match2:
        letter, num = match2.groups()
        for x in range(4):
            zs = '0' * x
            alt_ids.append('B%s%s%s' % (letter, zs, num))
        if len(num) < 3:
            num = '0' + num
        leg_id = 'B%s%s' % (letter, num)
        base_id = leg_id
    elif match3:
        letter, num = match3.groups()
        for x in range(4):
            zs = '0' * x
            alt_ids.append('G%s%s%s' % (letter, zs, num))
        if len(num) < 3:
            num = '0' + num
        leg_id = 'G%s%s' % (letter, num)
        base_id = leg_id
    elif match4:
        num = match4.groups()[0]
        for x in range(4):
            zs = '0' * x
            alt_ids.append('GLST%s%s' % (zs, num))
        if len(num) < 5:
            num = '0' + num
        leg_id = 'GLST%s' % num
        base_id = leg_id
    info = proposal.get(base_id)
    if info:
        prop_id = info.get('proposal_id', prop_id)
        leg_id = info.get('legacy_id', leg_id)
    if prop_id:
        prop_id = prop_id.upper()
    if leg_id:
        leg_id = leg_id.upper()
    if base_id:
        base_id = base_id.upper()
    record['proposal_id'] = prop_id
    record['legacy_id'] = legacy_id
    record['base_id'] = base_id
    record['alt_ids'] = [i.upper() for i in alt_ids]
    record['fetched_ids'] = True
    return

def proposal_id(record):
    """Get a proposal ID value given a scan dict record."""
    fetch_ids(record)
    return record.get('proposal_id')

def legacy_id(record):
    """Get a legacy ID value given a scan dict record."""
    fetch_ids(record)
    return record.get('legacy_id')

def doc_id(record):
    """Get an ID value for Solr given a scan dict record."""
    fetch_ids(record)
    base = record.get('base_id')
    scan = record.get('SCAN')
    if not is_a_value(base) or not is_a_value(scan):
        return None
    return base + '-' + scan

def session_id(record):
    """Get session ID (based on proposal ID) value given a scan dict record."""
    prop_id = proposal_id(record)
    pass
    return None

def alt_id(record):
    """Create alternate IDs (permute on non-alpha) given a scan dict record."""
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

def investigator_display(record):
    """Create an investigator display (proposal) given a scan dict record."""
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
    if not is_a_value(given):
        return None
    else:
        return float(given) / 1000.0

def skyfreq(record):
    """Get a skyfreq value given a scan dict record, convert Hz to GHz."""
    given = record.get('SKYFREQ')
    if not is_a_value(given):
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
    if not is_a_value(given):
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
    if not is_a_value(given):
        return None
    return float(given)

def doc_it(record):
    """Create a Solr doc (dict for pysolr) given a scan dict record."""
    d_id = doc_id(record)
    if not d_id:
        # ID is required.
        return {}
    ra, dec = ra_dec(record)
    items = [('id', d_id),
             ('telescope', 'GBT'), # TODO, really?  And, what of GBT+VLBA projects?
             ('proposal_id', proposal_id(record)),
             ('legacy_id', legacy_id(record)),
             ('session_id', session_id(record)),
             ('alt_id', alt_id(record)),
             ('title', title(record)),
             ('abstract', abstract(record)),
             ('pi', pi(record)),
             ('investigator', investigators(record)),
             ('investigator_display', investigator_display(record)),
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
             ('backend', record.get('config_backend')),
             ('bandwidth', bandwidth(record)),
             ]
    return dict([(k, v) for k, v in items if is_a_value(v)])

# Create generator for lazy iteration over all scans in CSV dump of GBT data.
docs = (doc_it(record) for record in csv.DictReader(open('data.csv')))
