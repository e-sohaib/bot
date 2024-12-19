import json
import re





with open('agahi.json' , 'r' ,encoding='utf-8') as l:
    X = l.read()
    
import re

# متن نمونه
text = '''
"action":{"type":"OPEN_POSTLIST_PAGE_GRPC", "payload":{"@type":"type.googleapis.com/widgets.OpenPostListPageGRPCPayload", "search_data":{"form_data":{"data":{"brand_model":{"repeated_string":{"value":["xiaomi"]}}, "category":{"str":{"value":"mobile-phones"}}}}}, "source_view":"CATEGORY_BREAD_CRUMB", "source_view_str":"CATEGORY_BREAD_CRUMB"}}}, {"title":"xiaomi redmi note 12 pro",
'''

# رجکس برای پیدا کردن مقدار مدل از "brand_model"
brand_model_pattern = r'"brand_model":\s*\{\s*"repeated_string":\s*\{\s*"value":\s*\[\s*"([^"]+)"\s*\]\s*\}'

# رجکس برای پیدا کردن عنوان مدل از "title"
title_pattern = r'"title":"([^"]+)"'

# پیدا کردن اولین مقدار "brand_model"
brand_model_match = re.search(brand_model_pattern, text)

# پیدا کردن اولین مقدار "title"
title_match = re.search(title_pattern, text)

# نمایش نتایج
if brand_model_match:
    print(f"اولین مدل (brand_model) یافت شد: {brand_model_match.group(1)}")
else:
    print("هیچ مقدار برای brand_model یافت نشد.")

if title_match:
    print(f"اولین عنوان مدل (title) یافت شد: {title_match.group(1)}")
else:
    print("هیچ مقدار برای title یافت نشد.")
  
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
