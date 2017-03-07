# passive-dns

## TL;DR

    passive_dns.py
    代码来自:
    利用scapy 造了一个Passive DNS Collector 工具——pdns_sniff
    作者：Komi
    https://github.com/coffeehb/tools/tree/master/pdns_sniff

    数据库存储改为MongoDB，运行于Python3

运行界面：
![image](https://github.com/tnt1200/passive-dns/raw/master/img/web.png)

## 环境搭建

### 安装MongoDB

安装mongodb,创建数据库目录：
```
brew install mongodb
mkdir -p /data/db
```

配置文件默认在 /usr/local/etc下的mongodb.conf文件，示例文件如下：
```
fork=true
dbpath = /data/db
logpath = /usr/local/var/log/mongodb/mongo.log
logappend = true
bind_ip=127.0.0.1
```

### 在OSX下安装python3.5
```
sudo port install python35
sudo port select --set python3 python35
```

### 安装virtualenvwrapper
```
sudo pip install virtualenvwrapper
```
编辑~/.profile文件，加入以下几行
```
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON="/Library/Frameworks/Python.framework/Versions/3.5/bin/python3"
source /Library/Frameworks/Python.framework/Versions/3.5/bin/virtualenvwrapper.sh
```
创建virtualenv
```
mkvirtualenv passivedns
```
安装库
```
pip3 install -r requirement.txt
```

## 使用

默认监听en0网卡，使用-i 指定网卡
```
python passive_dns.py -i en0
```
启动web服务
```
python web.py
```
访问http://127.0.0.1:8000 查看
