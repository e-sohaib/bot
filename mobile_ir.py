import requests
import json
import urllib.parse

def request_to_digikala(category , model):
    head = {"Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",}

    query = urllib.parse.quote(model.encode('utf-8'),safe='')
    params = {'q':query,
              'page':1}
    api_url = f"https://api.digikala.com/v1/categories/{category}/search/?q={query}&page=1"
    responce = requests.get(api_url ,headers=head)
    return api_url
def serch_in_site_mobie_ir(search : str):
    head = {"Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",}
    query = query = urllib.parse.quote(search.encode('utf-8'),safe='')
    serch_in_site = f"https://www.mobile.ir/phones/ajaxphonesearch.aspx?q={query}"
    #mobile = f"https://www.mobile.ir/phones/search.aspx?terms={brand}+{model.replace(' ' , '+')}&submit="
    res = requests.get(serch_in_site , headers=head)
    return res
