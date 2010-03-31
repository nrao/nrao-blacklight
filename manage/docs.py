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

id_sep = '_'

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

session_count_re = re.compile('(\d{2,5})[-|_](\d{1,3})$', re.I)

def fetch_ids(record):
    """Fetch/determine essential IDs given a scan dict record.

    Given complexity in dealing with IDs, this function has some side effects:
     * store proposal ID to record['proposal_id']
     * store legacy ID to record['legacy_id']
     * store session for document ID to record['session_id']
     * store some alternate IDs to record['alt_ids']
     * store a flag indicating fetched_ids to record['fetched_ids']

    There are several cases where document ID should be based on the legacy ID.
    As such, the logic is currently encoded up front in determining the IDs.
    """
    if record.get('fetched_ids', False):
        return
    given = record.get('PROJID')
    if not is_a_value(given):
        record['fetched_ids'] = True
        return
    given = given.strip()
    match1 = idcase1.search(given)
    match2 = idcase2.search(given)
    match3 = idcase3.search(given)
    match4 = idcase4.search(given)
    prop_id = None
    leg_id = None
    sess_id = None
    alt_ids = []
    if match1:
        trimester, num = match1.groups()
        if len(num) < 3:
            num = '0' + num
        prop_id = 'GBT/%s-%s' % (trimester, num)
        sess_id = prop_id
    elif match2:
        letter, num = match2.groups()
        for x in range(4):
            zs = '0' * x
            alt_ids.append('B%s%s%s' % (letter, zs, num))
        if len(num) < 3:
            num = '0' + num
        leg_id = 'B%s%s' % (letter, num)
        sess_id = leg_id
    elif match3:
        letter, num = match3.groups()
        for x in range(4):
            zs = '0' * x
            alt_ids.append('G%s%s%s' % (letter, zs, num))
        if len(num) < 3:
            num = '0' + num
        leg_id = 'G%s%s' % (letter, num)
        sess_id = leg_id
    elif match4:
        num = match4.groups()[0]
        for x in range(4):
            zs = '0' * x
            alt_ids.append('GLST%s%s' % (zs, num))
        if len(num) < 5:
            num = '0' + num
        leg_id = 'GLST%s' % num
        sess_id = leg_id
    info = proposal.get(sess_id)
    if info:
        prop_id = info.get('proposal_id', prop_id)
        leg_id = info.get('legacy_id', leg_id)
    if prop_id:
        prop_id = prop_id.upper()
    if leg_id:
        leg_id = leg_id.upper()
    if sess_id:
        sess_id = sess_id.upper()
    session_count_match = session_count_re.search(given)
    if session_count_match and len(session_count_match.groups()) > 1:
        session_count = session_count_match.groups()[-1]
        while len(session_count) < 2:
            session_count = '0' + session_count
        if len(session_count) > 2:
            if session_count[-3] == '0':
                session_count = session_count[-2:]
            else:
                session_count = session_count[-3:]
        if sess_id:
            sess_id = sess_id + id_sep + session_count
    else:
        sess_id = None
    if prop_id and not prop_id.startswith('None'):
        record['proposal_id'] = prop_id
    if leg_id and not leg_id.startswith('None'):
        record['legacy_id'] = leg_id
    if sess_id and not sess_id.startswith('None'):
        alt_ids.append(sess_id)
        record['session_id'] = sess_id.replace('/', '').replace('-', id_sep)
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

def session_id(record):
    """Get session ID (based on proposal ID) value given a scan dict record."""
    fetch_ids(record)
    return record.get('session_id')

def doc_id(record):
    """Get an ID value for Solr given a scan dict record."""
    fetch_ids(record)
    base = record.get('session_id')
    scan = record.get('SCAN')
    if not is_a_value(base) or not is_a_value(scan):
        return None
    while len(scan) < 3:
        scan = '0' + scan
    return base + id_sep + scan

def alt_id(record):
    """Create alternate IDs (permute on non-alpha) given a scan dict record."""
    fetch_ids(record)
    if record.has_key('alt_id'):
        return record['alt_id']
    alt_ids = record.pop('alt_ids', [])
    prop_id = record.get('proposal_id', '')
    leg_id = record.get('legacy_id', '')
    for x in (prop_id, leg_id,):
        alt_ids.append(x.replace('_', '-'))
        alt_ids.append(x.replace('-', '_'))
        alt_ids.append(x.replace('/', ''))
        alt_ids.append(x.replace('-', '').replace('_', ''))
        alt_ids.append(x.replace('/', '').replace('-', '').replace('_', ''))
    alt_ids = [i for i in alt_ids if i]
    record['alt_id'] = alt_ids
    return record['alt_id']

def get_proposal_info(record):
    """Get a dict of proposal info given a scan dict record."""
    fetch_ids(record)
    proposal_info = {}
    for key in ('proposal_id', 'legacy_id',):
        info = proposal.get(record.get(key))
        if info:
            proposal_info = info
            break
    if not proposal_info:
        for key in alt_id(record):
            info = proposal.get(key)
            if info:
                proposal_info = info
                break
    return proposal_info

def title(record):
    """Get the project title (proposal) given a scan dict record."""
    proposal_info = get_proposal_info(record)
    return proposal_info.get('title')

def abstract(record):
    """Get the project abstract (proposal) given a scan dict record."""
    proposal_info = get_proposal_info(record)
    return proposal_info.get('abstract')

def format_investigators(proposal_info, only_pi=False, mark_pi=False, m='**'):
    """Format investigators, return list of strings. Optionally mark PI."""
    pi = proposal_info.get('pi_details', {})
    guys = proposal_info.get('investigator_details', [])
    if only_pi:
        if pi:
            guys = [pi]
        else:
            pi = None
            guys = []
    formatted_guys = []
    for guy in guys:
        formatted_guy = '%s, %s (%s)' % (guy['last_name'],
                                         guy['first_name'],
                                         guy['affiliation'])
        if mark_pi and guy == pi:
            formatted_guy += m
        formatted_guys.append(formatted_guy)
    return sorted(formatted_guys)

def pi(record):
    """Get the project PI (proposal) given a scan dict record."""
    proposal_info = get_proposal_info(record)
    return ', '.join(format_investigators(proposal_info, only_pi=True))

def investigators(record):
    """Get the project investigators (proposal) given a scan dict record."""
    proposal_info = get_proposal_info(record)
    return format_investigators(proposal_info)

def investigator_display(record):
    """Create an investigator display (proposal) given a scan dict record."""
    proposal_info = get_proposal_info(record)
    return ', '.join(format_investigators(proposal_info, mark_pi=True))

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

ra_dec_expression = re.compile('J2000\s*@\s*\(([^,]*),\s*([^\)]*)\)')

def ra_dec(record):
    """Get a ra, dec value pair given a scan dict record."""
    loc = record.get('catalog_location')
    if (loc is None or loc == ''):
        return None, None
    match = ra_dec_expression.search(loc)
    if match:
        return match.groups()
    else:
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
