import json


with open('citys.txt' , 'r' , encoding='utf-8') as l:
    dics = json.load(l)
print(dics.keys())
print(dics['city'].keys())
print(dics['city']['topCities'])
cityscom = dics['city']['compressedData']
bigcitys = []
for item in cityscom:
    if item[0] < 100:
        bigcitys.append([item[1],item[2]])
print(len(bigcitys))
with open('bigcitys.json' , 'w' , encoding='utf-8') as l3:
    json.dump(bigcitys , l3 ,ensure_ascii=False ,indent=1)
#with open('citycomp.json' , 'w' , encoding='utf-8') as l2:
#    json.dump(cityscom , l2 ,ensure_ascii=False ,indent=4)
