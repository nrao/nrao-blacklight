import csv
import operator
import user

raw_docs = [record for record in csv.DictReader(open('data.csv'))]
docs = []

field_map = {'Instruments': ('12 Meter','36 Foot','85 Foot','140 Foot',
                             '300 Foot','Archival VLA','GBI','GBT',
                             'Technical','VLA','VLBA','VLBI','VSOP',
                             'Non-Observational','MK II Correlator',
                             'MK IV Correlator','20 Meter',),
             'Surveys': ('CGPS','VGPS','MAGPIS','NVSS','SPGS','FIRST',
                         'VGPS','MAGPIS','CGPS','SPGS','FIRST','HAS',),
             'NRAO Libraries': ('Charlottesville','Socorro','Green Bank',
                                'NRAO Library'),
             }

mapped_fields = reduce(operator.add, field_map.values())
mapped_fields += ('Other', 'Other (Write in)') # Other is an Instrument

# TODO Is there a better way?
def build_decade_lookup(begin, end):
    """Create a decade lookup table (dict)."""
    begin = int(begin)
    end = int(end)
    decade = {}
    decade_splits = range(begin, end+10, 10)
    decade_index = 1
    for year in range(begin, end, 1):
        if year > decade_splits[decade_index]:
            decade_index += 1
        start_year = decade_splits[decade_index-1] + 1
        end_year = decade_splits[decade_index]
        decade[year] = '%d - %d' % (start_year, end_year)
    return decade

decade = build_decade_lookup(1950, 2020)

def get_decade(year):
    """Provide a decade facet value given a year."""
    return decade.get(int(year), 'none')

# Heavily massage fields for creating dicts (pysolr) for Solr docs.
for raw_doc in raw_docs:
    doc = {'Title': '',
           'Author': '',
           'Institution': '',
           'Year': '',
           'Instruments': [],
           'Surveys': [],
           'Electronic Location': '',
           'ADS Bibcode': '',
           'Availability': [],
           'Notes': '',
           'PreDoc': '',
           }
    for k,v in [(k,v) for k,v in raw_doc.items() if k not in mapped_fields]:
        v = v or ''
        v = v.decode('latin1')
        doc[k] = v

    for key in field_map.keys():
        ks = field_map[key]
        doc[key] = [k for k,v in raw_doc.items() if k in ks and str(v) == 'TRUE']

    doc['Survey Facet'] = [survey for survey in doc['Surveys']]
    doc['Instrument Facet'] = [instrument for instrument in doc['Instruments']]

    other = raw_doc.get('Other (Write in)', '')
    if other:
        doc['Instruments'].append(other)
        doc['Instrument Facet'].append('Other')

    doc['id'] = doc.pop('Primary Key', '')
    doc['title_display'] = '%s / %s' % (doc['Title'], doc['Author'])
    doc['Electronic Location'] = doc['Electronic Location'].strip('#')

    formatted_doc = dict()
    for k,v in doc.items():
        formatted_doc[k.strip().lower().replace(' ', '_')] = v

    instruments_display = ', '.join(sorted(formatted_doc['instruments']))
    surveys_display = ', '.join(sorted(formatted_doc['surveys']))
    nrao_libraries_display = ', '.join(sorted(formatted_doc['nrao_libraries']))
    availability = []
    if formatted_doc.get('electronic_location', ''):
        availability.append('Online')
    if nrao_libraries_display:
        availability.append('NRAO Library')
    if not availability:
        availability = ['Not Available at NRAO']
    availability_display = ', '.join(availability)

    formatted_doc['instruments_display'] = instruments_display
    formatted_doc['surveys_display'] = surveys_display
    formatted_doc['nrao_libraries_display'] = nrao_libraries_display
    formatted_doc['availability'] = availability
    formatted_doc['availability_display'] = availability_display

    # if formatted_doc.get('year', ''):
    #     formatted_doc['date'] = '%s-01-01T00:00:00Z' % formatted_doc['year']
    if formatted_doc.get('electronic_location', ''):
        formatted_doc['electronic_status'] = 'Online'
        href = formatted_doc['electronic_location']
    if formatted_doc.get('ads_bibcode', ''):
        formatted_doc['ads_bibcode_status'] = 'Available'
    formatted_doc['decade_facet'] = get_decade(formatted_doc.get('year', 0))


    # Clean out fields which do not have values.
    [formatted_doc.pop(k) for k,v in formatted_doc.items()
     if v == '' or v is None]

    docs.append(formatted_doc)
