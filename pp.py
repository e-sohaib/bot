import json



with open('agahi.json' , 'r' ,encoding='utf-8') as l:
    X = json.load(l)
print(X['sections'][0]['widgets'][0]['data']["parent_items"][0]["action"]["payload"]["search_data"]["form_data"]['data']['category']['str']['value'])
#a = (X['list_widgets'])
#print(a[0].keys())
#print(a[1]['data'])
#with open('citys.txt' , 'r' , encoding='utf-8') as l:
#    dics = json.load(l)
#print(dics.keys())
#for item in dics['search']["rootCat"]["children"] :
#    print(item['name'])
#with open('category.json' ,'w' , encoding='utf-8') as ca:
#    json.dump(dics['search']["rootCat"]["children"] , ca ,ensure_ascii=False ,indent=2)
#print(dics['city'].keys())
#print(dics['city']['topCities'])
#with open('citys.txt' , 'r' ,encoding='utf-8') as l:
#    dics= json.load(l)
#cityscom = dics['city']['compressedData']
#bigcitys = []
#for item in cityscom:
#    if item[0] < 100:
#        bigcitys.append([item[1],item[0]])
#print(len(bigcitys))
#with open('bigcitys.json' , 'w' , encoding='utf-8') as l3:
#    json.dump(bigcitys , l3 ,ensure_ascii=False ,indent=1)
#with open('citycomp.json' , 'w' , encoding='utf-8') as l2:
#    json.dump(cityscom , l2 ,ensure_ascii=False ,indent=4)
