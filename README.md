## 通过python 和 selenium  抢大麦网演出票

### 1.安装依赖

1.安装python包（下载python可以直接下载anaconda）

```
pip install selenium
```

2.下载chromeDriverhttp://chromedriver.storage.googleapis.com/index.html，对应自己的chrome版本，将下载的chromeDriver放置到对应的python安装目录的Scripts文件夹下

### 2.变量修改

```
    self.loginId = 'account'
    self.loginPwd = 'password'
    self.itemId = '717541618637' #对应的要抢票的id
    self.classDate = '2023-07-16' #具体到天，如果演唱会只有1天，可以不选
    self.priceStr = '180' #票价
    self.ticketCount = 2
    self.viewers = ["鸣人", "佐助"]
    self.grabMinute = 0 # 抢票的时间分钟，在快要抢票的时候打开
```

将文件头部的变量修改为你需要抢票的对应的参数，然后运行 python damai.py