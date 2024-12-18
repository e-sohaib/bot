import json
import urllib.parse
with open('d.json' , 'r' , encoding='utf-8') as f:
    di = json.load(f)
    
print(di.keys())
print(di['list_widgets'][0].keys())
print(di['list_widgets'][0]['data']['action']['payload'])
token = di['list_widgets'][0]['data']['action']['payload']['token']
title = di['list_widgets'][0]['data']['action']['payload']['web_info']['title']
base = 'https://divar.ir/v/'
url = base +  title + '/' + token
print(url)
p = urllib.parse.quote(url.encode('utf-8'), safe='')
print(p)