# Bilibili-spyder
## ⚠️声明
1. **本项目仅供学习交流使用，请勿用于任何商业行为**
2. **如若本项目造成不良影响及后果与本人无关**
3. **如若侵权删**
****
## 介绍
本项目主要工作是分析哔哩哔哩评论区内容，将数据可视化
## 使用方法
1. 打开mian程序，按注释修改内容
    ```python
        referer = '' #链接
        oid = '' #评论区oid代码
        SESSDATA = '' #自己账号cookie
        
        #Type为评论区代码类型，需要修改
        C = comment(referer=referer, SESSDATA=SESSDATA, oid=oid, Type=17)
    ```
    评论区代码类型参考（[点击此处跳转](https://socialsisteryi.github.io/bilibili-API-collect/docs/comment/)）

2. 运行代码，错误会保存在同目录error.txt文件下,评论保存在./store/comment.json
3. 打开data_anlyze程序，找到以下代码，按注释修改内容
    ```python
        #需要分析的开始与结束时间格式20xx-xx-xx
        start_date = '2024-04-27' 
        end_date = '2024-05-01'
        #单位 'H'（每小时）'D'（每日）或 'M'（每月）以下例子是3小时为单位
        unit = '3H'
    ```
4. 运行data_anlyze, 生成分析图片，保存在同目录
### ⚠️警告
接口 https://api.bilibili.com/x/internal/gaia-gateway/ExClimbWuzhi payload 
大概目的应该是对特定的buvid(设备码) 进行risk检测
所以用多了大概率会有封禁措施，自己想办法绕过，这里不提供方法
[aa](https://github.com/MetaCubeX/ClashMetaForAndroid/releases/download/v2.10.1/cmfa-2.10.1-meta-x86_64-release.apk)
### 部分参考 
· [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
