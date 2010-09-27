import collections
import csv
import datetime
import itertools
import user

strptime = datetime.datetime.strptime

def format_datetime(datestring, strpformat='%y-%b-%d %H:%M:%S',
                    strfformat='%Y-%m-%dT%H:%M:%SZ'):
    return strptime(datestring, strpformat).strftime(strfformat)

def _obs(fd):
    for key, group in \
            itertools.groupby(csv.DictReader(fd, quoting=csv.QUOTE_NONE),
                              key=lambda x: x['project']):
        doc = collections.defaultdict(lambda: [])
        doc['id'] = key
        for record in group:
            tcsn = record.pop('tele_conf_sub_nant', '')
            (record['telescope'], record['configuration'],
             record['sub'], record['nant']) = tcsn.split(':')
            for key in record:
                if key in ('first', 'last',):
                    record[key] = format_datetime(record[key])
                doc[key] = doc[key] + [record[key]]
        yield dict(doc)

def _docs(obs_fd):
    for doc in _obs(obs_fd):
        yield doc

docs = _docs(open('archobs-project-sorted.csv'))

if __name__ == '__main__':
    count = 0
    for doc in docs:
        print doc['id']
        count += 1
    print count, 'docs'
