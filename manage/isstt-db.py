from os import environ, path

import _mysql

db = _mysql.connect(host='newsql5', db='isstt',
                    user='isstt', passwd='1ssttread')
db.set_character_set('utf8')

timestamp_path = path.join(environ['HOME'], '.isstt-latest')

# Soon this will hit a view with the following fieldnams.
# Use the following when the VIEW is available.
fields = ("fileName", "title", "authors", "firstAuthor", "altAuthors",
          "session", "firstPage", "lastPage", "procYear", "abstract",
          "created", "modified", "category1", "category2",)
select_fields = ','.join(fields)

try:
    timestamp = open(timestamp_path).read().strip()
except:
    where = ''
else:
    where = 'WHERE modified > "%s"' % timestamp

query = 'SELECT %s FROM paper_query %s;' % (select_fields, where)
db.query(query)

r = db.use_result()
row = r.fetch_row()
docs = []
while row:
    doc = dict(zip(fields, row[0]))
    docs.append(doc)
    row = r.fetch_row()

if docs:
    timestamps = [doc.get('modified', '') for doc in docs]
    if timestamps:
        print >>open(timestamp_path, 'w'), sorted(timestamps)[-1]

db.close()
