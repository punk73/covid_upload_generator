
import math
from nis import match
from operator import index
import pandas as pd
from datetime import datetime


def execute():
    file_name =  'test.xlsx'# path to file + file name
    sheet = datetime.today().strftime('%d%m%Y')  #'19082022'# sheet name or sheet number or list of sheet numbers and names

    print(sheet)
    try:
        df = pd.read_excel(io=file_name, sheet_name=sheet)
    except Exception as e:
        print(e)
        return False

    # print(df.head(5))  # print first 5 rows of the dataframe

    copy = df[['NO', 'STATUS EPIDEMIOLOGI SAAT INI', 'KESIMPULAN']]

    print(copy.head(5)) 

    copy.to_excel( sheet+ '.xlsx', index=False)

#  execute()
import re
import sys
# wa = input('input text wa :')
wa = sys.stdin.read()
matchs = re.findall('Total :\s+\d+', wa )

# print(wa)
res = {
    'konfirmasi': 0,
    'kontak_erat': 0,
    'probable': 0,
    'suspek': 0,
}

keys = [ "konfirmasi", "kontak_erat", "probable", "suspek" ]
temp = []
for matched in matchs:
    t = re.search('\d+', matched)
    temp.append(t.group(0))

i = 0
for key in keys:
    res[key] = int(temp[0])
    i = i+1

print(res)