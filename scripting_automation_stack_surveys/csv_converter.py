import csv
import math


# Path of the stack survey's csv results doc.
filename = ''
with open(filename, encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    dataType = {}
    maxCharValues = [0] * len(header)
    for col in reader:
        for i, el in enumerate(col):
            if not el.isnumeric():
                dataType[i] = 'char'
                maxCharValues[i] = max(len(el), maxCharValues[i])
            elif dataType.get(i, 0):
                maxCharValues[i] = max(len(str(el)), maxCharValues[i])

res = []
for i, col in enumerate(header):
    if not maxCharValues[i]:
        res.append(f"{col} INTEGER,")
    else:
        rounded = math.ceil(maxCharValues[i] / 10) * 10
        res.append(f"{col} VARCHAR,")

# Insert the path of the output here.
w_filename = ''
with open(w_filename, 'w') as f:
    for line in res:
        f.write(f"{line}\n")
