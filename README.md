# 说明文档

账号 xxxxxx的相关信息在tgconfigure.ini中 。 

id 获取方式
```bash
https://my.telegram.org/apps
```

程序执行完毕后导出的文件，部分用户的用户名为空
这是用户信息设置为Hidden的缘故。与数据拉取无关

## 获取群信息

使用Telegram API 

###  Telegram API 

- 代码文件telegramAPI.py

配置文件为tgconfigure.ini

账号，api_id,api_hash及其他写入.ini.  

#### 启动
```python
python3 telegramAPI.py
```

启动后会生成一个phonenumber的session文件。留着即可

控制台会显示让你输入Code，telegram客户端会收到验证码，如下

```bash
Login code: 91102. Do not give this code to anyone, even if they say they are from Telegram!

This code can be used to log in to your Telegram account. We never ask it for anything else.

If you didn't request this code by trying to log in on another device, simply ignore this message.

```
第一次启动输入91102 即可。

调用API，登陆账号后输出如下，选择一个ID进行数据导出。
```bash
Check api_id & api_hash first 
Set socks5 
Start!
        
[+] Choose a group to scrape members :
[0] - Digifinex & ICL
[1] - Bybit English
[2] - CoinMarketCap English
[3] - BitTorrent BTT
[4] - passive income5 group
[5] - Airdrop Official Community 🇮🇩
[6] - AscendEX English Official
[7] - LBank Official Group
[8] - Oasis Network Community
[9] - Tokocrypto Official Group 🌍 🇮🇩

[+] Enter a Number :
```
选择要输出的群ID号即可

比如输入测试群Test的ID  -  52.开始进行数据导出

导出文件为群名+群ID信息的CSV文件
```bash
Test_1613406438.csv
```

#### 内容如下
```bash
id,username
xxxx,SpamBot
xxxxx,builderwtfbot
xxxxx,huyyyyylalawao
```

- 第一行为id和username字段
- 第二行开始为导出的用户ID和用户名

如有需要也可以导出用户的其他信息比如手机号等

代码部分已注释！

### 登陆部分

国内登陆账号进行数据抓取数据需要使用SOCKS5进行代理

打开VPN查询代理服务器，写入.ini 配置文件中的proxy字段当中即可

### 数据抓取

telegram API 服务器对外部接口调用进行限制，群成员人数过一定人数时会进行限制，这个无法改不了，可查看官方文档。 

可以使用循环调取接口，但是只能进行字符串的匹配，群人数上万拉取数据比较耗时
且拉取群成员数据匹配只能达到80% ～95%

代码可查看`queryKey` 

匹配字段，中文不能全部匹配，英文可以用a-z
如果获取中文名为username的 querykey设置为 `''`即可。

启用注释掉的部分匹配度能提高很多，但是会更耗时

## 其他

Proxy 相关
For Python >= 3.6 : install python-socks[asyncio]
For Python <= 3.5 : install PySocks

TelegramClient('anon', api_id, api_hash, proxy=("socks5", '127.0.0.1', 4444))
