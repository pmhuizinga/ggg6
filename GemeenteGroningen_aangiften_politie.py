import urllib.request
import json
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import numpy as np

# aangiften politie: https://groningen.dataplatform.nl/#/data/f9861a56-4db6-414c-9b67-d79f2ef01d26?totalViews=10
url = "https://ckan.dataplatform.nl/api/action/datastore_search?resource_id=4a2051c6-b790-42de-bd42-f5033b51cc50"
url_parkeervakken = "https://ckan.dataplatform.nl/dataset/7ff17203-0dba-40f8-9abf-1b770baa6be6/resource/ed307596-cadd-4982-821c-29856260ae2e/download/parkeervakken_gem_groningen.json"

def handle_numbers(s):
    '''
    replace . with , in case of float (Dutch number notation)
    '''
    return float(str(s).replace('.', ''))


with urllib.request.urlopen(
        "https://ckan.dataplatform.nl/api/action/datastore_search?resource_id=4a2051c6-b790-42de-bd42-f5033b51cc50") as file:
    data = json.loads(file.read().decode(), parse_float=handle_numbers)
    df = json_normalize(data['result']['records']).dropna().drop(['_id'], axis=1)

# graph
plt.figure(figsize=(16, 10))
plt.boxplot(df.iloc[:, :-2])
plt.xlabel('Aangifte')
plt.ylabel('Aantal')
plt.xticks(range(1, df.shape[0] + 1, 1), df.iloc[:, -2].tolist(), rotation=45, rotation_mode="anchor")
plt.show()

# graph
plt.figure(figsize=(16, 10))
plt.bar(df.iloc[:, :-2].columns, df.iloc[:, :-2].sum())
plt.show()

# graph
x = np.array(range(1996, 2018))
y = np.array(df[df['aangifte'] == 'diefstal fiets'].iloc[:, :-2]).reshape(22, )
plt.plot(x, y)
plt.show()


#********************8
with urllib.request.urlopen(url_parkeervakken) as file:
    data = json.loads(file.read().decode(), parse_float=handle_numbers)

for feature in data['features']:
    print feature['geometry']['type']
    print feature['geometry']['coordinates']