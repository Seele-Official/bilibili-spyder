import csv
import Func
import json

class comment(Func.bili):
    def __init__(self, referer, SESSDATA, oid, Type) -> None:
            Func.bili.__init__(self)
            self.__oid = oid
            self.__referer = referer
            self.__SESSDATA = SESSDATA
            self.__type = Type
            self.__offset = '{"offset":""}'
            self.headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'origin': 'https://www.bilibili.com',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': self.__referer,
                'sec-ch-ua': '"Google Chrome";v="120", "Chromium";v="120", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
            nav = self.nav_init(self.headers)
            self.img_key = nav['img_key']
            self.sub_key = nav['sub_key']

    def refresh(self):
        cookies = {
            'SESSDATA': self.__SESSDATA,
            'buvid3':self.Buvid3
        }
        params = {
            'oid': self.__oid,
            'type': self.__type,
            'mode': '2',
            # sort mode , default 3
            # 0 3：only hot
            # 1：hot + time
            # 2：only time
            'pagination_str': self.__offset,
            'plat': '1',
            'web_location': '1315875',
        }
        params = self.wbi_sign(params=params, img_key=self.img_key, sub_key=self.sub_key)
        res = self.Get_with_exception(url='https://api.bilibili.com/x/v2/reply/wbi/main', params=params, cookies=cookies, headers=self.headers)
        temp = res.json()
        if temp['data']['cursor']['is_end']:
             return False
        self.__offset = \
                        '{"offset":"' + \
                        json.dumps(temp['data']['cursor']['pagination_reply']['next_offset']).strip('"') + \
                        '"}'
        print(self.__offset)
        return temp
    def comment_reply(self, oid, rpid, pn):
        cookies = {
        }


        params = {
            'oid': oid,
            'type': self.__type,
            # 评论区类型代码 https://socialsisteryi.github.io/bilibili-API-collect/docs/comment/
            'root': rpid, 
            #rpid
            'ps': '20',
            # 每页项数	非必要	默认为20
            # 定义域：1-49
            #  data_replies 的最大内容数为20,因此设置为49其实也只会有20条回复被返回
            'pn': pn,
            # num	页码	非必要	默认为1
            'gaia_source': 'main_web',
            'web_location': '333.788',
        }
        params = self.wbi_sign(params=params, img_key=self.img_key, sub_key=self.sub_key)

        response = self.Get_with_exception('https://api.bilibili.com/x/v2/reply/reply', params=params, cookies=cookies, headers=self.headers)
        return response.json()
    def get_reply_comments(self, oid, rpid):
        replies = []
        num = 1
        while(True):
            res = C.comment_reply(oid=oid, rpid=rpid, pn=num)
            count = res['data']['page']['count']
            num = res['data']['page']['num']
            replies += res['data']['replies']
            print(num*20, count, rpid)
            if (count <= num*20):
                break
            num += 1
            
        return replies


if __name__ == '__main__':
    referer = ''
    oid = ''
    SESSDATA = ''
    
    
    C = comment(referer=referer, SESSDATA=SESSDATA, oid=oid, Type=17)
    replies = []
    while(True):
        res = C.refresh()
        if(res):
            replies += res['data']['replies']
        else:
            break
    
    for index, reply in enumerate(replies):
        oid = reply['oid']
        rpid = reply['rpid']
        # see if the reply has any comments.
        if reply['rcount'] > 0:
            reply_comments = C.get_reply_comments(oid=oid, rpid=rpid)
            replies[index]['replies'] = reply_comments
    filename = "comment"
    with open(f'./store/{filename}.json','w+',encoding='utf-8',errors='ignore') as f:
        f.write(json.dumps({
            'data':replies
        }))
         

    
