## 简述

通过Internet对客户端的软件进行远程升级的框架。
主要利用TCP/IP编程技术，进行服务器端和客户端的通信与传输。

## 构成

### 服务器端

1. 文件结构

```
+---server
    |   config.ini                  # 配置文件
    |   calc_md5.py                 # 计算文件md5值的工具
    |   dss_autoupdate_server.py    # 服务器端推送服务
    |
    \---sv_package
            xxxx.1.0.0              # 软件包
```

2. 功能
    - 打开Socket连接，监听特定端口
    - 获取最新软件包信息，发送给客户端
    - 如有需要，推送软件包

### 客户端

1. 文件结构

```
+---client
    |   config.ini                  # 配置文件
    |   calc_md5.py                 # 计算文件md5值的工具
    |   dss_autoupdate_client.py    # 客户端自动更新软件
    |
    \---cl_package
            xxxx.0.9.0              # 软件包
```

2. 功能
    - 打开Socket连接服务器
    - 从服务器端获取最新软件包信息，与本地最新作比较
    - 如有需要，接受最新软件包
    - 展开软件包，替换旧版本

### 时序图

![](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=dGl0bGUgT1RB5pe25bqP5Zu-CgphY3RvciBVc2VyCgoKVXNlci0-Q2xpZW50OiDlkK_liqjoh6rliqjmm7TmlrDnqIvluo8KCgAcBi0-U2VydmVyOiDlu7rnq4tUQ1Dov57mjqUAFworABkJj5HpgIHmoKHpqoznoIEKADQGLT4tAGUI6L-U5ZueABoHu5PmnpwAMxPor7fmsYLmnIDmlrDova_ku7bljIXkv6Hmga8AORkAGBUgCgoKYWx0IOacieaWsOeJiOacrAogICAgAIEwCVVzAGsGoumXruaYr-WQpumcgOimgQCCAwYAJwUAgigGAIEzDwCBNQcgICAgAEwFYWx0IAAuDAAQBgBeDQCBQR0AJgkAgiER5o6o6YCBABcYAIMbCAAlCQCCdgUAdAkAfQkAggEFAIMSBemAmui_hwCBFgkAMRTlsZXlvIAAgQoSAFwVm7_mjaLml6cAglMLAG0RZWxzZQCBFAflpLHotKUANB-05pawABYTAEYKbmQAgVESAIUeEACEPweWreW8gACCThEAhUoJhbPpl60AhUkHAIIpDQCBLwXkuI0Ag38RACJKAIE_CAoAghoGl6AAhQ8WAIE4GQCBLCEKZW5kCgo&s=modern-blue)

## 通信定义

### 请求与返回

1. 客户端请求

```
req = {
    'request' : value，
    'data' : {}
}
```

| request value | description |
| ----- | ----------- |
| handshake | 比对data内容，通过后才能继续 |
| header | 请求最新版本信息 |
| package | 请求软件包 |
| exit | 断开连接 |

2. 服务端返回

```
resp = {
    'response' : value,
    'data' : {}
}
```

| response value | description |
| ----- | ----------- |
| connected | 连接成功 |
| error | 错误 |
| header | 最新版本信息 |
| package | 后续数据是软件包 |

data 的可能项目：

```
    'latest' : filename
    'size' : size
    'md5' : md5
```

## 使用示例
### 一、 环境要求
#### Server端

- 支持Python3以上的OS
- Python3以上版本（开发环境为Python 3.8）
- 能够访问
	- 如在外网，需要固定外网IP或者域名
	- 如在内网，需要固定内网IP
- 防火墙需要打开通信端口

#### Client端

- 支持Python3以上的OS（假定开发板子安装Linux系统）
- Python3以上版本（开发环境为Python 3.8）
- 能够访问到Server的网络
- 需要Python模块[tqmd](https://github.com/tqdm/tqdm)
- 防火墙需要打开通信端口

### 二、 配置文件

**必须在运行前正确配置两端的`config.ini`文件。**
Server端与Client端使用同一个配置文件。内容及说明如下：

```
#############################################
#
# Server端和Client端通用设置
#
#############################################
[DEFAULT]

# 端口设置，需要在防火墙打开该端口才能通信
# 取值范围 1000~65535
port = 1234

# 传输缓存
buffer_size = 1024

# 验证
security = password

#############################################
#
# Server端配置
#
#############################################
[Server]

# Server端ip，留空代表可接受任意值
ip =

# 软件包存放路径，注意区分绝对路径与相对路径
path = sv_package

# 最新软件包名称
latest = xxxx.1.0.0

# 最大同时连接数
max_clients = 5


#############################################
#
# Client端配置
#
#############################################
[Client]

# Server端ip，可以用域名
server = laobaitu.xyz

# Client端接受软件包存放路径，注意区分绝对路径与相对路径
path = cl_package

# 最新软件包名称
latest = xxxx.0.9.0

# 接受文件后操作，包括解压，部署，重启等
after_proccess = after_proccess.sh

```

>[info] 在Client端对比最新软件包名称来决定是否有新版本软件。

### 三、 启动Server端
1. 前面在`config.ini`中配置了软件包路径和名称，将该名称的软件包放入该路径中。
2. 终端里导航到server目录。
```
cd /home/laobaitu/server
```
3. 执行 dss_autoupdate_server.py
```
python dss_autoupdate_server.py
```
此时服务启动，由于是死循环，需要`Ctrl+C`来终止该服务。
也可以将服务放置于后台执行。
```
nohup python dss_autoupdate_server.py & 
```
4. 此时Server端会有输出提示在已监听端口
```
[INFO] 2021-03-23 14:05:22,152 Attempt to bind IP/Port: :1234
```
5. Server端启动完成。

### 四、 Client端的运行
1. 正确配置`config.ini`文件。
2. 终端里导航到client目录。
```
# 在编写该文档时用了Windows系统做示例
cd "D:\Work\DSS GUI\OTA\framework\client"
```
3. 执行 dss_autoupdate_client.py
```
python dss_autoupdate_client.py
```
4. 此时会尝试与Server端通信并检查更新。
5. 如果有更新，会提示确认：
```
[INFO] 2021-03-23 13:13:26,425 Current version is: Python-3.9.0.tgz ...
[INFO] 2021-03-23 13:13:26,425 Upgrade available. Latest is: Python-3.9.2.tgz ...
Do you want to upgrade to latest? (y/n)y
```
6. 确认后会下载最新的软件包。

### 五、 总体
正常运行OTA框架后，在Server端和Client端会输出类似以下的日志。
```
######### Server端 #######
[INFO] 2021-03-23 14:13:19,016 Attempt to bind IP/Port: :1234
[INFO] 2021-03-23 14:13:25,262 Accept new connection from 116.236.49.163:25178...
[INFO] 2021-03-23 14:13:26,279 [<-('116.236.49.163', 25178)] Recieved data is : {'request': 'handshake', 'data': {'security': 'password'}} ...
[INFO] 2021-03-23 14:13:26,279 [('116.236.49.163', 25178)] Checking security code {password} VS {password} ...
[INFO] 2021-03-23 14:13:26,279 [->('116.236.49.163', 25178)] Send SecurityCheck response {'response': 'connected', 'data': {}} ...
[INFO] 2021-03-23 14:13:26,359 [<-('116.236.49.163', 25178)] Recieved data is : {'request': 'header', 'data': {}} ...
[INFO] 2021-03-23 14:13:26,359 [->('116.236.49.163', 25178)] Send latest package header info: {'response': 'header', 'data': {'latest': 'Python-3.9.2.tgz'}} ...
[INFO] 2021-03-23 14:15:44,612 [<-('116.236.49.163', 25178)] Recieved data is : {'request': 'package', 'data': {}} ...
[INFO] 2021-03-23 14:15:44,710 [->('116.236.49.163', 25178)] Send latest package file: {'response': 'package', 'data': {'latest': 'Python-3.9.2.tgz', 'size': '25399571', 'md5': '8cf053206beeca72c7ee531817dc24c7'}} ...
[INFO] 2021-03-23 14:15:45,711 [->(116.236.49.163, 25178)] Sending...
[INFO] 2021-03-23 14:15:55,746 [<-('116.236.49.163', 25178)] Recieved data is : {'request': 'exit', 'data': {}} ...
[INFO] 2021-03-23 14:15:55,746 Exit proccess ...
[INFO] 2021-03-23 14:15:55,746 Connection from 116.236.49.163:25178 closed.

```
然后Server端会继续等待下一次Client的连接。

```
######### Client端 #######
[INFO] 2021-03-23 13:13:25,139 Reading configuration from: config.ini ...
[INFO] 2021-03-23 13:13:25,147 Connect to server/port: laobaitu.xyz:1234 ...
[INFO] 2021-03-23 13:13:26,248 Send { {'request': 'handshake', 'data': {'security': 'password'}} 
} to server ...
[INFO] 2021-03-23 13:13:26,344 Response from server is: {'response': 'connected', 'data': {}} ...[INFO] 2021-03-23 13:13:26,344 Send { {'request': 'header', 'data': {}} } to server ...
[INFO] 2021-03-23 13:13:26,424 Response from server is: {'response': 'header', 'data': {'latest': 'Python-3.9.2.tgz'}} ...
[INFO] 2021-03-23 13:13:26,425 Current version is: Python-3.9.0.tgz ...
[INFO] 2021-03-23 13:13:26,425 Upgrade available. Latest is: Python-3.9.2.tgz ...
Do you want to upgrade to latest? (y/n)y
[INFO] 2021-03-23 13:15:44,596 Ready to upgrade soon...
[INFO] 2021-03-23 13:15:44,596 Send { {'request': 'package', 'data': {}} } to server ...
[INFO] 2021-03-23 13:15:44,774 Response from server is: {'response': 'package', 'data': {'latest': 'Python-3.9.2.tgz', 'size': '25399571', 'md5': '8cf053206beeca72c7ee531817dc24c7'}} ...        
100%|██████████████████████████████████████████| 25399571/25399571 [00:09<00:00, 2583319.16it/s] 
[INFO] 2021-03-23 13:15:55,728 MD5 check success. Latest package is cl_package\Python-3.9.2.tgz ...
[INFO] 2021-03-23 13:15:55,730 Send { {'request': 'exit', 'data': {}} } to server ...
```

>[To-Do] 到目前，OTA流程已经进行到下载最新软件包。后续需要制作软件包的解压，部署工作，这部分操作需要调用`after_proccess.sh`来完成，接下来的目标。