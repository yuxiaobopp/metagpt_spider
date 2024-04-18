#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/6 14:13
@Author  : alexanderwu
@File    : llm_hello_world.py
"""
import asyncio

from metagpt.llm import LLM
from metagpt.logs import logger
import httpx
from fake_useragent import UserAgent
import os
import time
from pathlib import Path
import json
headers = {
    "user-agent": UserAgent().random,
}
params = {
    "wd": "python"  # 输入百度搜索的内容
}
def parse_timestamp(time_stamp, flag=True):
        """
        把时间戳转换为时间字符串
        :param time_stamp: 时间戳
        :param flag: 标志位，可以指定输出时间字符串的格式
        :return: 时间字符串,格式为：2019-01-01 12:12:12 或 2019-01-01
        """
        localtime = time.localtime(time_stamp)
        if flag:
            time_str = time.strftime("%Y_%m_%d_%H_%M_%S", localtime)
        else:
            time_str = time.strftime("%Y_%m_%d", localtime)
        return time_str
async def main():
    # 调用爬虫工具
    savedata_dir=os.getcwd()+"/data/weibodata"
    os.makedirs(savedata_dir, exist_ok=True)
    base_url='https://m.weibo.cn/api/container/getIndex?sudaref=cn.bing.com&display=0&retcode=6102&containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot'
    resp = httpx.get(base_url, params=None, headers=headers, cookies=None, proxies=None)  # 和原来requests的使用方法类似
    resp.encoding = resp.charset_encoding  # 根据文档的编码还对文档进行编码
    name=parse_timestamp(time.time(),flag=True)
    file_name = os.path.join(savedata_dir, name+ '.txt')
    Path(file_name).write_text(resp.text)
    # print(json.loads(resp.text)['data']['cards'])
    data_list=json.loads(resp.text)['data']['cards']
    topwords=''
    for d in data_list:
        try:
            if 'card_group' in d:
                group_data=d['card_group']
                for g in group_data:
                    # 判断字典是否存在desc
                    if 'desc' in g:
                        print(g['desc'])
                        if g['desc'] =='查看更多文娱热搜':
                            continue
                        topwords=topwords+g['desc']+'\n'
        except Exception as e:
            print('===================')
    # 保存爬取的信息
    file_name = os.path.join(savedata_dir, name+ '_topwords.txt')
    Path(file_name).write_text(topwords)
    # 交给gpt流程化
    # 定义流程角色 
    # Action1 读取数据,分类
    

    # Action2 根据分类数据向量搜索
    # Action3 给大模型做分析给出答案

    llm = LLM()
    # llm type check
    


if __name__ == "__main__":
    asyncio.run(main())
