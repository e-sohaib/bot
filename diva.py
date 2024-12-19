import json
import urllib.parse
with open('a.txt' , 'r' , encoding='utf-8') as f:
    di = json.load(f)
#print(di.keys())
file = di['data']
print(file.keys())

print(file['products'][0].keys())
print(file['filters'])
          

#for item in di['sections'][4]['widgets']:
#    try:
#        if item['data']['title'] == 'قیمت':
#            price = item['data']['value']
#    except:
#        price = None
#        continue
#        
#    try:
#        if item['data']['title'] ==  'مقدار رم':
#            ram = item['data']['value']
#    except:
#        ram = None
#        continue
#    try:
#        if item['data']['title'] ==  'رنگ':
#            color = item['data']['value']
#    except:
#        color = None
#        continue
#    try:    
#        if item['data']['title'] ==  'حافظهٔ داخلی':
#            hard_space = item['data']['value']
#    except:
#        hard_space = None
#        continue
#print(price , ram , color , hard_space)
#    #print(item)
#print('*'*50)
#print(di['sections'][4]['widgets'][0]['action_log']['server_side_info']['info']['brand'])
#print(di['sections'][4]['widgets'][0]['action_log']['server_side_info']['info']['model'])