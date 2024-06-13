import random
import requests
import time
import urllib.parse
import re
from hashlib import md5

class bili:
    def handle_exception(self, error):
        filename = 'error.txt'
        with open(filename, mode='a+',encoding='utf-8') as f:
            f.write(str(error) + '\n')
    def Get_with_exception(self, url, headers, params, cookies):
        try:
            response = requests.get(url=url, headers=headers, params=params, cookies=cookies, timeout=3)
            # if res_status isn't 200，throw HTTPError exception
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            input('enter to continue')
            self.handle_exception(http_err)
            self.Get_with_exception(url=url, headers=headers, params=params, cookies=cookies)
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            input('enter to continue')
            self.handle_exception(timeout_err)
            self.Get_with_exception(url=url, headers=headers, params=params, cookies=cookies)
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            input('enter to continue')
            self.handle_exception(req_err)
            self.Get_with_exception(url=url, headers=headers, params=params, cookies=cookies)
        else:
            print(f"Success! Status Code: {response.status_code} {time.time()}")
            code = response.json()['code']
            error_messages = {
                -400: "请求错误",
                -404: "无此项",
                12002: "评论区已关闭",
                12009: "评论主体的type不合法",
                # -403 : '权限不足'
            }
            if code != 0:
                if code in error_messages:
                    self.handle_exception(f'{code} {error_messages[code]}')
                    print(error_messages[code])
                else:
                    print(f'{code} 未知的错误代码')
                    self.handle_exception(f'{code} 未知的错误代码')
                input('enter to continue')
            return response
    def randomhex(self,n):
        s = ''
        for i in range(n):
              s += random.choice('0123456789ABCDEF')
        return s
    def buvid3(self):
         e = self.randomhex
         t = random.randint(0,99999)
         return f'{e(8)}-{e(4)}-{e(4)}-{e(4)}-{e(12)}{t:5>0}infoc'
    def getPictureHashKey(self, raw_wbi_key: bytes):
        Z = [
            46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42,
            19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60,
            51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52,
        ]
        
        mixin_key = ''.join(chr(raw_wbi_key[n]) for n in Z)[:32]
        
        return mixin_key
    def wbi_sign(self, params: dict, img_key: str, sub_key: str):
        H = self.getPictureHashKey((img_key + sub_key).encode())
        K = round(time.time())
        params = {**params, "wts": K}
        params = dict(sorted(params.items()))

        ne = []
        te = re.compile(r"[!'()*]")
        
        # sort key and filter out "!'()*" chars
        for key in params:
            value = params[key]
            if isinstance(value, str):
                value = te.sub('', value)
            if value is not None:
                encoded_key = urllib.parse.quote(key, safe='')
                encoded_value = urllib.parse.quote(str(value), safe='')
                ne.append(f"{encoded_key}={encoded_value}")
        ee = "&".join(ne)
        params = {**params, "w_rid": md5((ee + H).encode()).hexdigest()}

        return params
    def nav_init(self, headers:dict):
        cookies = {
            # self.SESSDATA
        }

        res = requests.get('https://api.bilibili.com/x/web-interface/nav', cookies=cookies, headers=headers).json()
        wbi = res['data']['wbi_img']
        return {
            'img_key' : wbi['img_url'].split('/')[-1].split('.')[0],
            'sub_key' : wbi['sub_url'].split('/')[-1].split('.')[0]  
        }
       
    def __init__(self) -> None:
         self.Buvid3 = self.buvid3()