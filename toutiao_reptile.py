import pymysql
import requests
import json
from openpyxl import workbook
import time
import hashlib
import os
import datetime
import pandas as pd

start_url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time='
url = 'https://www.toutiao.com'

headers = {
    'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_12_3) applewebkit/537.36 (khtml, like gecko) chrome/71.0.3578.98 safari/537.36'
}
cookies = {'tt_webid': '6691095209642165771'}  # 此处cookies可从浏览器中查找，为了避免被头条禁止爬虫

max_behot_time = '0'  # 链接参数
title = []  # 存储新闻标题
source_url = []  # 存储新闻的链接
s_url = []  # 存储新闻的完整链接
source = []  # 存储发布新闻的公众号
comments_number = []
media_url = {}  # 存储公众号的完整链接


def get_as_cp():  # 该函数主要是为了获取as和cp参数，程序参考今日头条中的加密js文件：home_4abea46.js
    zz = {}
    now = round(time.time())
    # print(now)  # 获取当前计算机时间
    e = hex(int(now)).upper()[2:]  # hex()转换一个整数对象为16进制的字符串表示
    # print('e:', e)
    a = hashlib.md5()  # hashlib.md5().hexdigest()创建hash对象并返回16进制结果
    # print('a:', a)
    a.update(str(int(now)).encode('utf-8'))
    i = a.hexdigest().upper()
    # print('i:', i)
    if len(e) != 8:
        zz = {'as': '479bb4b7254c150',
              'cp': '7e0ac8874bb0985'}
        return zz
    n = i[:5]
    a = i[-5:]
    r = ''
    s = ''
    for i in range(5):
        s = s + n[i] + e[i]
    for j in range(5):
        r = r + e[j + 3] + a[j]
    zz = {
        'as': 'a1' + s + e[-3:],
        'cp': e[0:3] + r + 'e1'
    }
    # print('zz:', zz)
    return zz


def getdata(url, headers, cookies):  # 解析网页函数
    r = requests.get(url, headers=headers, cookies=cookies)
    # print(url)
    data = json.loads(r.text)
    return data

def main(max_behot_time, title, source_url, s_url, source, comments_number, media_url):  # 主函数
    # print(media_url)
    for i in range(10):  # 此处的数字类似于你刷新新闻的次数，正常情况下刷新一次会出现10条新闻，但夜存在少于10条的情况；所以最后的结果并不一定是10的倍数
        ascp = get_as_cp()  # 获取as和cp参数的函数
        # url = start_url+max_behot_time+'&max_behot_time_tmp='+max_behot_time+'&tadrequire=true&as='+ascp['as']+'&cp='+ascp['cp']
        # print(url)
        demo = getdata(
            start_url + max_behot_time + '&max_behot_time_tmp=' + max_behot_time + '&tadrequire=true&as=' + ascp[
                'as'] + '&cp=' + ascp['cp'], headers, cookies)
        # print(demo)
        time.sleep(3.5)  # 设置睡眠,以免爬太快被封ip
        for j in range(len(demo['data'])):
            # print(demo['data'][j]['title'])
            if demo['data'][j]['title'] not in title:
                title.append(demo['data'][j]['title'])  # 获取新闻标题
                source_url.append(demo['data'][j]['source_url'])  # 获取新闻链接
                source.append(demo['data'][j]['source'])  # 获取发布新闻的公众号
                if 'comments_count' in demo['data'][j]:
                    comments_number.append(demo['data'][j]['comments_count'])
                else:
                    comments_number.append('没有评论')
            if demo['data'][j]['source'] not in media_url:
                media_url[demo['data'][j]['source']] = url + demo['data'][j]['media_url']  # 获取公众号链接
        # print(max_behot_time)
        max_behot_time = str(demo['next']['max_behot_time'])  # 获取下一个链接的max_behot_time参数的值
        for index in range(len(title)):
            print('标题：', title[index])
            if 'https' not in source_url[index]:
                s_url.append(url + source_url[index])
                print('新闻链接：', url + source_url[index])
            else:
                print('新闻链接：', source_url[index])
                s_url.append(source_url[index])
            # print('源链接：', url+source_url[index])
            print('头条号：', source[index])
            print('评论数:', comments_number[index])
            print('------------华丽分割线-------------')
        # print('头条号链接：', media_url[index])
        title = []
        s_url = []
        source = []
        comments_number = []

if __name__ == '__main__':
    main(max_behot_time, title, source_url, s_url, source,comments_number, media_url)
