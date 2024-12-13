import requests
import json
import datetime
import time


def request_to_api(city_number , category_realname):
    raw_header = {"Accept": "*/*",
               "Accept-Encoding": "deflate, gzip",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
               "Host": "api.divar.ir",
               "Content-Type": "application/json",
               "Content-Length": "444"}
    current_time = datetime.datetime.utcnow().isoformat()+'Z'
    raw_data = {"city_ids":[city_number],"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":current_time,"page":1,"layer_page":1,},"search_data":{"form_data":{"data":{"category":{"str":{"value":category_realname}}}},"server_payload":{"@type":"type.googleapis.com/widgets.SearchData.ServerPayload","additional_form_data":{"data":{"sort":{"str":{"value":"sort_date"}}}}}}}
    data = json.dumps(raw_data)
    api_address = 'https://api.divar.ir/v8/postlist/w/search'
    response = requests.post(url=api_address , data=data ,headers=raw_header)
    time.sleep(3)
    return response.text
    

         
         

        
        
    

    