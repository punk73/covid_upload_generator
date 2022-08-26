
from linecache import getline
import pandas as pd
from datetime import datetime
import re
import sys
import os
from pathlib import Path
import glob

def getLatestExcel():
    downloads_path = str(Path.home() / "Downloads/*.xlsx" )
    search_dir = downloads_path #'./'
    files = glob.glob(search_dir ) #filter(os.path.isfile, os.listdir(search_dir))
    files = [os.path.join(search_dir, f) for f in files]  # add path to each file
    # files.sort(key=lambda x: os.path.getmtime(x))
    # files = [f for f in files if f[-4:] == 'xlsx']
    files_xls = max(files, key = os.path.getmtime )
    return files_xls

def generateCopy(filenameParams=None, sheetParams=None):
    file_name = filenameParams if filenameParams else  getLatestExcel()# path to file + file name
    
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
Sheetname = input('input sheetname :')
if Sheetname == '':
    Sheetname = None
    
res = generateCopy(sheetParams=Sheetname)

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