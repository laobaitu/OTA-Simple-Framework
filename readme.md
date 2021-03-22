# 用Python搭建的简易OTA框架
## 简述

通过Internet对客户端的软件进行远程升级的框架。
主要利用TCP/IP编程技术，进行服务器端和客户端的通信与传输。

## 构成

### 服务器端

1. 文件结构

```
+---server
    |   config.ini                  # 配置文件
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
    'request' : value
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