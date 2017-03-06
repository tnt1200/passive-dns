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

## 安装

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
安装库
```
pip3 install -r requirement.txt
```

## 使用

默认监听en0网卡，使用-i 指定网卡
```
python3 passive_dns.py -i en0
```
启动web服务
```
python3 web.py
```
访问http://127.0.0.1:8000 查看
