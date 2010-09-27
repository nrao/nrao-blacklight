import csv
import re
import sys

def records(fd, **kwargs):
    start_re = re.compile('^.*(ngas_.*)$')
    time_re = re.compile('^\d\d\:\d\d:\d\d$')
    band_re = re.compile('^([A-Za-z]{1,2} )*([A-Za-z]{1,2})$')
    num_re = re.compile('^\d\d+$')
    sep_re = re.compile('####')

    row = []
    for line in csv.reader(fd, **kwargs):
        for field in line:
            # print row, field
            field = field.strip()
            if not field:
                continue
            start_match = start_re.match(field)
            if start_match is not None:
                row = [start_match.group(1)]
                continue
            if time_re.match(field) is not None:
                row[-1] += ' ' + field
                continue
            if sep_re.match(field) is not None:
                # If we have more than 14 fields, something went wrong.
                if len(row) > 14:
                    # Fix the case where a obs band names are split.
                    maybe_bands = row[9] + ' ' + row[10]
                    if band_re.match(maybe_bands) is not None:
                        row = row[:9] + [maybe_bands] + row[11:]
                if len(row) > 14:
                    # Fix the case where a project name with a space is split.
                    if num_re.match(row[13]) is None:
                        row = row[:12] + [row[12] + ' ' + row[13]] + row[14:]
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
