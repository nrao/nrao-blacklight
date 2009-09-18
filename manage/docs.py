import csv
import operator

raw_docs = [record for record in csv.DictReader(open('data.csv'))]
docs = []

field_map = {'Instruments': ('12 Meter','36 Foot','85 Foot','140 Foot',
                             '300 Foot','Archival VLA','GBI','GBT',
                             'Technical','VLA','VLBA','VLBI','VSOP',
                             'Non-Observational','MK II Correlator',),
             'Surveys': ('CGPS','VGPS','MAGPIS','NVSS','SPGS','FIRST',),
             'NRAO Libraries': ('Charlottesville','Socorro','Green Bank',),
             }

mapped_fields = reduce(operator.add, field_map.values())
mapped_fields += ('Other', 'Other (Write in)')

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
           'NRAO Libraries': [],
           'Notes': '',
           'PreDoc': '',
           }
    for k,v in [(k,v) for k,v in raw_doc.items() if k not in mapped_fields]:
        v = v or ''
        v = v.decode('latin1')
        doc[k] = v

    for key in field_map.keys():
        ks = field_map[key]
        doc[key] = [k for k,v in raw_doc.items() if k in ks and str(v) == '1']

    doc['Survey Facet'] = [survey for survey in doc['Surveys']]
    other = raw_doc.get('Other (Write in)', '')
    if other:
        doc['Surveys'].append(other)
        doc['Survey Facet'].append('Other')

    doc['id'] = doc.pop('Primary Key', '')
    doc['title_display'] = '%s / %s' % (doc['Title'], doc['Author'])
    doc['Electronic Location'] = doc['Electronic Location'].strip('#')

    formatted_doc = dict()
    for k,v in doc.items():
        formatted_doc[k.strip().lower().replace(' ', '_')] = v

    instruments_display = ', '.join(sorted(formatted_doc['instruments']))
    surveys_display = ', '.join(sorted(formatted_doc['surveys']))
    nrao_libraries_display = ', '.join(sorted(formatted_doc['nrao_libraries']))

    formatted_doc['instruments_display'] = instruments_display
    formatted_doc['surveys_display'] = surveys_display
    formatted_doc['nrao_libraries_display'] = nrao_libraries_display

    [formatted_doc.pop(k) for k,v in formatted_doc.items() if not v]

    # if formatted_doc.get('year', ''):
    #     formatted_doc['date'] = '%s-01-01T00:00:00Z' % formatted_doc['year']
    if formatted_doc.get('electronic_location', ''):
        formatted_doc['electronic_status'] = 'online'
    if formatted_doc.get('ads_bibcode', ''):
        formatted_doc['has_ads_bibcode'] = True

    docs.append(formatted_doc)
