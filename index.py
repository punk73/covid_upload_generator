
import pandas as pd
from datetime import datetime
import re
import sys

def generateCopy(filenameParams=None, sheetParams=None):
    file_name = filenameParams if filenameParams else  'test.xlsx'# path to file + file name
    sheet = sheetParams if sheetParams else datetime.today().strftime('%d%m%Y')  #'19082022'# sheet name or sheet number or list of sheet numbers and names

    print('prepare for copy excel file '+ file_name + ' with sheetname '+ sheet )
    try:
        df = pd.read_excel(io=file_name, sheet_name=sheet)
    except Exception as e:
        print(e)
        return False

    # print(df.head(5))  # print first 5 rows of the dataframe

    copy = df[['NO', 'STATUS EPIDEMIOLOGI SAAT INI', 'KESIMPULAN']]

    konfirmasi  = len(df[df['STATUS EPIDEMIOLOGI SAAT INI']=='KONFIRMASI'])
    kontak_erat = len(df[df['STATUS EPIDEMIOLOGI SAAT INI']=='KONTAK ERAT'])
    probable    = len(df[df['STATUS EPIDEMIOLOGI SAAT INI']=='PROBABLE'])
    suspek      = len(df[df['STATUS EPIDEMIOLOGI SAAT INI']=='SUSPEK'])

    res = {"konfirmasi":konfirmasi, "kontak_erat":kontak_erat,"probable": probable, "suspek":suspek}
    # print(copy.head(5)) 
    copy.to_excel( sheet+ '.xlsx', index=False)
    return res

#  execute()


def getWaStr():
    print('insert WA content :')
    print('click ctrl+D after you paste the content!')
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
        res[key] = int(temp[i])
        i = i+1

    return res

# wa = getWaStr()

wa = getWaStr()
res = generateCopy()

# print(res)
for key in res :
    if res[key] != wa[key] :
        print("VALIDATION ERROR! "+key+" WA:"+str(wa[key])+ " file:"+str(res[key]) )
        # raise Exception('key tidak sama.' + key)
        sys.exit()

print(res)
print(wa)
print('data sama! lanjutkan!')
# print(result)