import requests
import json
import sys
print("start")
mid = "473518575"
WORKDIC = sys.argv[0].split('likes.py')[0]
BV=WORKDIC+'bv.txt'
VIDEOINFOURL = 'https://api.bilibili.com/x/space/arc/search?mid='
upmid = "258457966"
data={
    'pn':1,
    'type':1,
    'oid':885818868
}
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Connection': 'keep-alive',
    'content-length': '101',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': '*******************',
    'host': 'api.bilibili.com',
    'Origin': 'https://www.bilibili.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}
def likesPlus(oid,rpid):
    likesData = {
        'oid': oid,
        'type': 1,
        'rpid': rpid,
        'action': 1,
        'csrf': '**********'
    }
    likesReq = requests.post("https://api.bilibili.com/x/v2/reply/action", data=likesData, headers=headers)
    print(likesReq.text)
    return json.loads(likesReq.text)['code']
def getFiletxt(path):
    return open(path, 'r').read().split('\n')[0:-1]
getUPInfo = requests.get(VIDEOINFOURL+upmid+"&pn=1&ps=50&index=1&jsonp=jsonp")
getAllvideoList = json.loads(getUPInfo.text)['data']['list']['vlist'][::-1]
bvlist = getFiletxt(BV)
for i in range(0,len(getAllvideoList)):
    if(getAllvideoList[i]['bvid'] not in bvlist):
        oid = getAllvideoList[i]['aid']
        req = requests.get("https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid="+str(oid))
        list = json.loads(req.text)['data']['replies']
        if(list is None):
            print("该视频还没有评论")
            continue
        for j in list:
            if(j['member']['mid']==mid):
                rpid = j['rpid']
                print(j['content']['message'])
                if(likesPlus(oid=oid, rpid=rpid)==0):
                    open(BV, 'a').write(getAllvideoList[i]['bvid'] + '\n')
                else:
                    print("end by error code")
                    exit(0)

print("end")