import collections
import copy
import csv
import datetime
import itertools
import sys
import user

strptime = datetime.datetime.strptime

def format_datetime(datestring, strpformat='%y-%b-%d %H:%M:%S',
                    strfformat='%Y-%m-%dT%H:%M:%SZ'):
    return strptime(datestring, strpformat).strftime(strfformat)

def groupby(fd, doc_factory):
    for key, group in itertools.groupby(
        csv.DictReader(fd, quoting=csv.QUOTE_NONE),
        key=lambda x: x['arch_file_id']):
        yield doc_factory(key, group)

def obs_factory(key, group):
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
    doc.pop('arch_file_id', None)
    return dict(doc)

def obs(fd):
    return groupby(fd, obs_factory)

def files_factory(key, group):
    records = list(group)
    if not records:
        raise ValueError, 'record %s has no data' % str(key)
    elif len(records) > 1:
        last_record = copy.deepcopy(records[0])
        last_record.pop('file_root', None)
        for record in records:
            current_record = copy.deepcopy(record)
            current_record.pop('file_root', None)
            if current_record != last_record:
                raise ValueError, 'record %s is inconsistent' % str(key)
    doc = records[0]
    doc['id'] = key
    doc['file_roots'] = [doc['file_root'] for record in records]
    return doc

def files(fd):
    return groupby(fd, files_factory)

def merge_docs():
    obs_docs = obs(open('archobs-fileid-sorted.csv'))
    files_docs = files(open('archfiles-fileid-sorted.csv'))
    files_table = {}
    for files_doc in files_docs:
        files_table[files_doc['id']] = files_doc

    for obs_doc in obs_docs:
        doc = obs_doc
        key = doc['id']

        # Verify consistency of project IDs.
        project = doc['project'][0]
        for i in range(1, len(doc['project'])):
            if doc['project'][i] != project:
                raise ValueError, 'record %s is inconsistent' % str(key)

        # Verify consistency of multiValued field lengths.
        length = None
        for k in doc:
            if k in ('id',): # exclude non-multiValued fields
                continue
            if length is None:
                length = len(doc[k])
            if len(doc[k]) != length:
                raise ValueError, 'record %s is inconsistent' % str(key)

        # Integrate with record from archfiles.
        files_doc = files_table.get(key, {})
        if files_doc:
            doc.update(files_doc)
            yield doc
        else:
            print >>sys.stdout, 'Warning: no archive file data for', key

docs = merge_docs()

if __name__ == '__main__':
    # obs_ids = set()
    # for doc in obs(open('archobs-fileid-sorted.csv')):
    #     obs_ids.add(doc['id'])
    # files_ids = set()
    # for doc in files(open('archfiles-fileid-sorted.csv')):
    #     files_ids.add(doc['id'])
    # print len(set.intersection(obs_ids, files_ids))
    # 2382 on 2010-09-27

    count = 0
    for doc in docs:
        print doc['id']
        count += 1
    print count, 'docs'
