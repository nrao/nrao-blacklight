import csv
import re
import sys

def records(fd, **kwargs):
    time_re = re.compile('\d\d\:\d\d:\d\d')
    polar_re = re.compile('([RL]{2} ?){1,4}$')

    row = []
    for line in csv.reader(fd, **kwargs):
        for field in line:
            # print row, field
            field = field.strip()
            if not field:
                continue
            if time_re.match(field):
                row[-1] += ' ' + field
                continue
            if polar_re.match(field) and polar_re.match(row[-1]):
                row[-1] += ' ' + field
                continue
            if len(row) == 16:
                tokens = field.split(' ')
                row.append(tokens[0])
                yield row
                if len(tokens) > 1:
                    row = [' '.join(tokens[1:])]
                else:
                    row = []
            else:
                row.append(field)


writer = csv.writer(sys.stdout, quotechar='`')
infile = open('fixme.csv')

try:
    for record in records(infile, quotechar='`'):
        writer.writerow(record)
except (KeyboardInterrupt, IOError):
    pass
