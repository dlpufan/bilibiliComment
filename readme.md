# **脚本中的csrf获取方式为** #

1.打开谷歌/火狐浏览器，按下f12，在f12中选择network，随便进入b站一个视频

![点开视频](https://img.fybgame.top/github/1.png)

2.发送一条评论，network中会多出几条请求，其中请求地址为https://api.bilibili.com/x/v2/reply/add  的请求中会有你的csrf，cookie获取方式同理！

![csrf](https://img.fybgame.top/github/2.png)

![cookie](https://img.fybgame.top/github/3.png)
