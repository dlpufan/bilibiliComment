import requests
import time
import json
import re
import os
import datetime
mid = '258457966'
VIDEOCOUNT = '/home/videoCount.txt'
BV = '/home/bv.txt'
FANSCOUNT = '/home/fansCount.txt'
VIDEOSENDTIME = '/home/lastSendTime.txt'
DataList = [VIDEOCOUNT,BV,FANSCOUNT,VIDEOSENDTIME]
VIDEOINFOURL = 'https://api.bilibili.com/x/space/arc/search?mid='
def init():
    for i in DataList:
        if(os.path.exists(i)==bool('')):
            open(i,'w').write('\n')

def getVideoTime(BV):
    str1 = requests.get('https://www.bilibili.com/video/' + BV).text
    m = re.search("(\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2})", str1)
    strdate = m.group(1)
    return strdate

def getCurrentTime():
    return time.strftime("%Y-%m-%d", time.localtime())

def getFiletxt(path):
    return open(path, 'r').read().split('\n')[0:-1]

def getTodaySendVideo():
    return getFiletxt(VIDEOCOUNT)[-1].split(" ")[1]

def getVideoInfo(count):
    pn = int((count-1)/50)+1
    playsum = 0;
    commentsum = 0;
    for i in range(0,pn):
        if i == (pn-1):
            r = json.loads(requests.get(
                VIDEOINFOURL + mid + '&pn=' + str(i + 1) + '&ps=' + str(
                    count % 50) + '&index=1&jsonp=jsonp').text)
        else:
            r = json.loads(requests.get(
                VIDEOINFOURL + mid + '&pn=' + str(i + 1) + '&ps=50&index=1&jsonp=jsonp').text)
        for i in r['data']['list']['vlist']:
            playsum += int(i['play'])
            commentsum += int(i['comment'])
    return [str(playsum),str(commentsum)]
def getTimeBeginLast(time):
    pattern = r'[-| |:]'
    result = [int(i) for i in re.split(pattern, time)]
    result2 = [int(i) for i in re.split(pattern, open(VIDEOSENDTIME,'r').read().split('\n')[0])]
    open(VIDEOSENDTIME,'w').write(time)
    seconds = (datetime.datetime(result[0],result[1],result[2],result[3],result[4],result[5])-datetime.datetime(result2[0],result2[1],result2[2],result2[3],result2[4],result2[5])).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d时%02d分%02d秒" % (h, m, s)

init()
req = requests.get(VIDEOINFOURL+mid+'&pn=1&ps=5&index=1&jsonp=jsonp')

getAllvideoList = json.loads(req.text)['data']['list']['vlist'][::-1]

bvlist = getFiletxt(BV)
for i in range(0, len(getAllvideoList)):
    aid = getAllvideoList[i]['aid']
    vdTime = getVideoTime(getAllvideoList[i]['bvid'])
    if (vdTime.split(' ')[0] != getCurrentTime()):
        continue;
    if (getAllvideoList[i]['bvid'] not in bvlist):
        open(BV, 'a').write(getAllvideoList[i]['bvid'] + '\n')
        videoCountStr = getFiletxt(VIDEOCOUNT)
        if (videoCountStr[-1].find(getCurrentTime()) == -1):
            open(VIDEOCOUNT, 'a').write(getCurrentTime() + " 1\n")
        else:
            videoCountStr[-1] = getCurrentTime() + " " + str(int(videoCountStr[-1].split(' ')[1]) + 1)
            resultTxt = ''
            for i in videoCountStr:
                resultTxt += i + "\n"
            file = open(VIDEOCOUNT, 'w')
            file.write(resultTxt)
            file.close()
        lastfans = int(open(FANSCOUNT, 'r').read())
        nowfans = (json.loads(requests.get('http://api.bilibili.com/x/relation/stat?vmid='+mid).text)['data']['follower'])
        open(FANSCOUNT, 'w').write(str(nowfans))
        videoInfoList = getVideoInfo(int(getTodaySendVideo()))
        message = '303是元老\nyb游戏菌为您服务\n---------------------------------\n今天是 '+getCurrentTime()+'\n---------------------------------\n这是up主卧龙寺今天发布的第'+getTodaySendVideo()+'个视频\n'+'距离发布上个视频涨粉'+str(nowfans - lastfans)+'\n'+'从今天0点到现在视频总播放量为'+videoInfoList[0]+'\n'+'从今天0点到现在视频总评论数为'+videoInfoList[1]+'\n'+'距离发布上个视频过去了'+getTimeBeginLast(vdTime)+'\n---------------------------------'
        print(message)
        postData = {
            'oid': aid,
            'type': '1',
            'message': message,
            'plat': '1',
            'ordering': 'heat',
            'jsonp': 'jsonp',
            'csrf': '****************' #此处填写自己的csrf，具体方式见readme.md
        }

        headers = {
            'authority': 'api.bilibili.com',
            'method': 'POST',
            'path': '/x/v2/reply/add',
            'scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'content-length': '101',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '****************', #此处填写自己的cookie，具体方式见readme.md
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        sendMessage = requests.post(url='https://api.bilibili.com/x/v2/reply/add', data=postData, headers=headers)
        print(sendMessage.text)






