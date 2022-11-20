import csv
import math


filename = '../survey2018/survey_results_public.csv'
with open(filename) as f:
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
        res.append(f"{col} INT,")
    else:
        rounded = math.ceil(maxCharValues[i] / 10) * 10
        res.append(f"{col} CHAR({rounded}),")

w_filename = 'result'
with open(w_filename, 'w') as f:
    for line in res:
        f.write(f"{line}\n")
    