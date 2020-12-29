import requests
import time
import json
import re
import os
import datetime
import sys
mid = '434294917'
UPNAME = '智障姬'

WORKDIC = sys.argv[0].split('bilibili.py')[0]
VIDEOCOUNT = WORKDIC+'videoCount.txt'
contrastDic = '/home/videoCount.txt'
#这个是卧龙寺发布的视频量的txt文件，去掉message中的getTodaySendVideo(contrastDic)，这个py文件就可以独立运行了
BV = WORKDIC+'bv.txt'
FANSCOUNT = WORKDIC+'fansCount.txt'
VIDEOSENDTIME = WORKDIC+'lastSendTime.txt'
NETWORKVIDEOCOUNT = 5
DataList = [VIDEOCOUNT,BV,FANSCOUNT,VIDEOSENDTIME]
VIDEOINFOURL = 'https://api.bilibili.com/x/space/arc/search?mid='
print()
def init():
    for i in DataList:
        if(os.path.exists(i)==bool('')):
            open(i,'w')

def getVideoTime(BV):
    str1 = requests.get('https://www.bilibili.com/video/' + BV).text
    m = re.search("(\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2})", str1)
    strdate = m.group(1)
    return strdate
def isTodayVideo(BV):
    str1 = requests.get('https://www.bilibili.com/video/' + BV).text
    m = re.search("(\d{4}-\d{1,2}-\d{1,2})", str1)
    return m.group(1)==getCurrentTime()

def getCurrentTime():
    return time.strftime("%Y-%m-%d", time.localtime())

def getFiletxt(path):
    return open(path, 'r').read().split('\n')[0:-1]

def getTodaySendVideo(path):
    return getFiletxt(path)[-1].split(" ")[1]
def getTodaySendVideoByNetwork():
    i = 0
    count = 0
    while True:
        i = i + 1
        r = json.loads(requests.get(
            VIDEOINFOURL + mid + '&pn=' + str(i) + '&ps=50&index=1&jsonp=jsonp').text)
        if(isTodayVideo(r['data']['list']['vlist'][-1]['bvid'])):
            count=count+50
        else:
            for j in r['data']['list']['vlist']:
                if(isTodayVideo(j['bvid'])):
                    count=count+1
                else:
                    return count
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
def getFansCount(mid):
    return (json.loads(requests.get('http://api.bilibili.com/x/relation/stat?vmid='+mid).text)['data']['follower'])
def getTimeBeginLast(time):
    pattern = r'[-| |:]'
    result = [int(i) for i in re.split(pattern, time)]
    try:
        result2 = [int(i) for i in re.split(pattern, open(VIDEOSENDTIME,'r').read().split('\n')[0])]
    except:
        result2 = result
    open(VIDEOSENDTIME,'w').write(time)
    seconds = (datetime.datetime(result[0],result[1],result[2],result[3],result[4],result[5])-datetime.datetime(result2[0],result2[1],result2[2],result2[3],result2[4],result2[5])).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d时%02d分%02d秒" % (h, m, s)

init()
req = requests.get(VIDEOINFOURL+mid+'&pn=1&ps='+str(NETWORKVIDEOCOUNT)+'&index=1&jsonp=jsonp')

getAllvideoList = json.loads(req.text)['data']['list']['vlist'][::-1]

bvlist = getFiletxt(BV)
for i in range(0, len(getAllvideoList)):
    aid = getAllvideoList[i]['aid']
    # if (vdTime.split(' ')[0] != getCurrentTime()):
    #     continue;
    if (getAllvideoList[i]['bvid'] not in bvlist):
        vdTime = getVideoTime(getAllvideoList[i]['bvid'])
        open(BV, 'a').write(getAllvideoList[i]['bvid'] + '\n')
        videoCountStr = getFiletxt(VIDEOCOUNT)
        if (len(videoCountStr)==0):
            open(VIDEOCOUNT, 'a').write(getCurrentTime() + " "+str(getTodaySendVideoByNetwork()-NETWORKVIDEOCOUNT+1)+"\n")
        elif (videoCountStr[-1].find(getCurrentTime()) == -1):
            open(VIDEOCOUNT, 'a').write(getCurrentTime() + " 1\n")
        else:
            videoCountStr[-1] = getCurrentTime() + " " + str(int(videoCountStr[-1].split(' ')[1]) + 1)
            resultTxt = ''
            for vcs in videoCountStr:
                resultTxt += vcs + "\n"
            file = open(VIDEOCOUNT, 'w')
            file.write(resultTxt)
            file.close()
        if(open(FANSCOUNT, 'r').read()!=''):
            lastfans = int(open(FANSCOUNT, 'r').read())
        else:
            lastfans = getFansCount(mid)
        nowfans = getFansCount(mid)
        open(FANSCOUNT, 'w').write(str(nowfans))
        videoInfoList = getVideoInfo(int(getTodaySendVideo(VIDEOCOUNT)))
        message = '---------------------------------\n今天是 '+getCurrentTime()+'\n---------------------------------\n这是up主'+UPNAME+'今天发布的第'+getTodaySendVideo(VIDEOCOUNT)+'个视频\n'+'（隔壁卧龙寺发了'+getTodaySendVideo(contrastDic)+'个)\n'+'距离发布上个视频涨粉'+str(nowfans - lastfans)+'\n'+'从今天0点到现在视频总播放量为'+videoInfoList[0]+'\n'+'从今天0点到现在视频总评论数为'+videoInfoList[1]+'\n'+'距离发布上个视频过去了'+getTimeBeginLast(vdTime)+'\n---------------------------------\nyb游戏菌统计完毕！不喜欢可以拉黑~'
        print(message)
        postData = {
            'oid': aid,
            'type': '1',
            'message': message,
            'plat': '1',
            'ordering': 'heat',
            'jsonp': 'jsonp',
            'csrf': '*************'
        }

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'Connection':'keep-alive',
            'content-length': '101',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '**************************',
            'host': 'api.bilibili.com',
            'Origin':'https://www.bilibili.com',
            'Referer':'https://www.bilibili.com/video/'+getAllvideoList[i]['bvid'],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
        }
        sendMessage = requests.post(url='https://api.bilibili.com/x/v2/reply/add', data=postData, headers=headers)
        print(sendMessage.text)






