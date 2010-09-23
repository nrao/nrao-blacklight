import csv
import re
import sys

def records(fd, **kwargs):
    time_re = re.compile('^\d\d\:\d\d:\d\d$')
    sep_re = re.compile('####')

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
            if sep_re.match(field):
                yield row
                row = []
            else:
                row.append(field)


print >>sys.stdout, ('file_root,logical_file,lock_status,project_code,segment,'
                     'starttime,stoptime,filesize,telescope:config,obs_bands,'
                     'format,calib,raw_project_code,arch_file_id')

writer = csv.writer(sys.stdout, quotechar='`')

# Copy input archfiles* to archfiles.txt, removing the header.
infile = open('archfiles.txt')

try:
    for record in records(infile, quotechar='`'):
        writer.writerow(record)
except (KeyboardInterrupt, IOError):
    pass
