import json
import csv
import sys


tsv_path = sys.argv[1]
out_path = sys.argv[2]

data = []

with open(tsv_path, 'r') as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    for row in tsvreader:
        
        data.extend(row)


print(len(data))

with open(out_path, 'w') as f:
        for item in data:
            i = json.loads(item)
            json.dump(i, f)
            f.write('\n')