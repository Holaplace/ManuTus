![https://github.com/Holaplace/ManuTus/blob/master/ManuTus.jpg?raw=true](https://github.com/Holaplace/ManuTus/blob/master/ManuTus.jpg?raw=true)

Table of Contents
=================

      * [ManuTus]()
         * [<g-emoji class="g-emoji" alias="memo" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4dd.png">📝</g-emoji> 关于](#关于)
         * [<g-emoji class="g-emoji" alias="rocket" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f680.png">🚀</g-emoji> 进展](#进展)
         * [<g-emoji class="g-emoji" alias="pushpin" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f4cc.png">📌</g-emoji> 操作指南]()
            * [Linux (Centos 7)](#Linux (Centos 7))
               * [Step 1 依赖安装](#Step 1 依赖安装)
               * [Step 2 安装配置 Python 3.5 以上](#Step 2 安装配置 Python 3.5 以上)
               * [Step 3 安装第三方库](#Step 3 安装第三方库)
               * [Step 4 上传Chromium 及 配置ManuTus (类型: .py) 文件](#Step 4 上传Chromium 及 配置ManuTus (类型: .py) 文件)
               * [常见问题](#常见问题)
         * [<g-emoji class="g-emoji" alias="building_construction" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f3d7.png">🏗</g-emoji> 附件下载](附件下载)

## ManuTus


### :pencil: 关于
ManuTus (Manuscript Status) 时刻监视投稿期刊的状态.

实现论文状态改变时，及时通过短信或电话通知作者.

### :rocket: 进展
欢迎对本项目提交“Issues”帮助我完善脚本;

目前支持**Elsevier**和**RSC**的投稿系统, 其它系统等有投稿再update哈...



### :pushpin: 操作指南
#### Linux (Centos 7)

##### Step 1 依赖安装

% 依赖库:
```
sudo yum install pango.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXext.x86_64 libXi.x86_64 libXtst.x86_64 cups-libs.x86_64 libXScrnSaver.x86_64 libXrandr.x86_64 GConf2.x86_64 alsa-lib.x86_64 atk.x86_64 gtk3.x86_64 nss.x86_64 -y
```
% 字体
```
sudo yum install ipa-gothic-fonts xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc -y
```
% 去沙箱
```
await launch ("--no-sandbox")
```

##### Step 2 安装配置 Python 3.5 以上

% 安装必要工具 yum-utils
```
sudo yum install yum-utils
```
% 使用yum-builddep为 Python3 构建环境
```
sudo yum-builddep python
```
% 下载 Python 3.7 源码包
```
sudo yum install wget
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```
% 编译安装Python 3.7
```
tar xf Python-3.7.0.tgz
cd Python-3.7.0
./configure
make && make install
```
% 升级 pip3
```
pip3 install --upgrade pip
```
##### Step 3 安装第三方库
% 安装库文件
```
pip3 install pyppeteer
pip3 install twilio
pip3 install baidu-aip
```
% 修改 pyppeteer 中的 connection.py 源码
```
文件位置: /usr/local/lib/python3.7/site-packages/pyppeteer/connection.py
修改参考: https://github.com/miyakogi/pyppeteer/pull/160/files

修改内容: 44行
	原: self._url, max_size=None, loop=self._loop)
	后: self._url, max_size=None, loop=self._loop, ping_interval=None, ping_timeout=None)
```
##### Step 4 上传Chromium 及 配置ManuTus (类型: .py) 文件
% 按照 **“附件下载”** 部分执行 (GFW的Linux可忽略)
% 使用 SFTP 软件挂载上传至 /home/
% 建立screen 多窗口控制, 以防退出SSH时, 任务中止.

```
screen -S name 建立name任务
screen -x name 进入name任务
screen -ls     浏览当前所有任务
crtl + A + D   返回主窗口

crontab -l     浏览当前所有定时任务
crontab -e     建立定时任务

*/15 * * * * python /home/manuOCR.py
*/17 * * * * python /home/RSC_VPS.py
```


**Note:** 

Elsevier--> manuOCR.py

RSC --> RSC_VPS.py

使用前提: 你已知晓如何申请[百度AI识别](https://login.bce.baidu.com/)和[Twilio](https://www.twilio.com/), 相关配置请Google.



##### 常见问题
1. Python环境设置, 出现在./configure末. 提示代码: -zlib not available (zipimport.ZipImportError: can‘t decompress data; zlib not available)

解决办法: 安装依赖后, 重新 make && make install
```
sudo yum install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev
```
2. 安装完 Python3 后, yum无法使用

解决方法: 修改yum的相关依赖,下述文件第一行改为 /usr/bin/python3.7
```
vi /usr/libexec/urlgrabber-ext-down
```


### :building_construction: 附件下载
如果在GFW内，首次执行pyppeteer时，无法完成下载Chromium. 故提供下载所需Chromium文件, 并将其移动到下解压 (之后可删除压缩包).

**LInux (CentOS 7) 文件, /root/.local/share/...**

链接: https://pan.baidu.com/s/14yyKZfBsR_fPKGX5MLowVQ 提取码: qdap

**Windows 10 文件, C:\Users\你的用户名\AppData\Local\pyppeteer\pyppeteer\\local-chromium\575458\\...**

*<u>downloadLink 1</u>*

https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/575458/chrome-win32.zip

*<u>downloadLink 2</u>*

链接: https://pan.baidu.com/s/1QagNo8EE5IO0apYPJn80JQ 提取码: ek1n



**Note:** 如果不存放在指定文件夹内, 只要在launch里配置一下Chromium的路径即可 (注意Linux和Windows路径斜线不同). 示例: 

*<u>Win</u>*

```
'executablePath': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', 
```

*<u>Linux</u>* 

```
'executablePath': '/root/home/chrome.exe',
```
