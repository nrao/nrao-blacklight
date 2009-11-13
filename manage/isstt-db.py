from os import environ, path

import _mysql

db = _mysql.connect(host='newsql4', db='isstt',
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

# Uncomment this when VIEW is available.
# query = 'SELECT %s FROM paper_query %s;' % (select_fields, where)
# db.query(query)

# Delete the following when VIEW is available.
# For now, build a query with multiple tables.
papers_fields = ("fileName", "title", "authors", "firstAuthor", "altAuthors",
                 "session", "firstPage", "lastPage", "procYear", "abstract",
                 "created", "modified",)
papers_select = ','.join(['papers.%s' % f for f in papers_fields])

sessions_fields = ("category1", "category2",)
sessions_select = ','.join(['sessions.%s' % f for f in sessions_fields])

select_fields = '%s,%s' % (papers_select, sessions_select)

join = 'papers.session = sessions.sesNo AND papers.procYear = sessions.procYear';
if not where:
    where = 'WHERE %s' % join
else:
    where = 'WHERE %s AND papers.modified > "%s"' % (join, timestamp)

query = 'SELECT %s FROM papers,sessions %s;' % (select_fields, where)
db.query(query)
# Now back to business.

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
