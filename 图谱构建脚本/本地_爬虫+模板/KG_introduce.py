# encoding=utf8
#这个脚本用来补全知识的介绍，
from urllib import request
from urllib.request import build_opener,ProxyHandler
import requests
import random
import jieba
import re
import logging
import json
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship

# User_Agent列表
user_agent_list = [
    "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
    "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
    "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
]

# 产生一个随机User-Agent
headers ={
    'User-Agent':random.choice(user_agent_list),
    'Connection': 'close'
}

#获取每个知识url列表
def get_article_url2(url,serv,serv_dic):
	req = requests.get(url,headers=headers)
	content = json.loads(req.text)
	for ele in content['result_vos']:
		order_detail(ele['url'],serv,serv_dic)
	req.close()

def order_detail(url2,serv,serv_dic):
	# print(url2)
	req2 = requests.get(url2,headers=headers)
	# 发送请求
	soup2 = BeautifulSoup(req2.text, 'html.parser')
	article2 = soup2.select('article p')
	# txt2 = re.split('。|！|？',"你好！我是笑。你是谁？")
	# print("：：：".join(txt2))
	for ele in article2:
		txt = ele.get_text()
		txt = txt.strip().replace(" ","").replace("\xa0","")
		txt = txt.lower()
		txt2 = re.split('。|！|？',txt)
		for ele2 in txt2:
			#采用摸版1
			#server_detail_rule1(url2,ele2,serv,serv_dic)
			comd_detail_rule1(url2,ele2,serv,serv_dic)

def server_detail_rule1(url2,ele2,serv,serv_dic):
	if ele2 == (serv+"是什么") or ele2 == (serv+"服务是什么"):
		return
	elif serv+"服务是" in ele2:
		print(ele2)
		add2dic(serv,serv_dic,ele2)
	elif serv+"是" in ele2:
		print(ele2)
		add2dic(serv,serv_dic,ele2)

def comd_detail_rule1(url2,ele2,serv,serv_dic):
	if ele2 == (serv+"是什么") or ele2 == (serv+"命令是什么") or ele2 ==(serv+"是什么？"):
		return
	else:
		every = re.split(',|，',ele2)
		for every_one in every:
			if every_one.startswith(serv+"命令是"):
				print(ele2)
				add2dic(serv,serv_dic,ele2)


#向字典添加元素
def add2dic(serv,tech_dic,commond):
	if commond in tech_dic[serv]:
		tech_dic[serv][commond] = tech_dic[serv][commond] + 1
	else:
		tech_dic[serv][commond] = 1

logging.basicConfig(filename = "./file/serv_detail.log",level = logging.CRITICAL)
logger = logging.getLogger()
#字典：用来存储服务与detail的次数关系：{"cron":{"crond":10,"vi":1}}
serv_dic={}
# tech_f = open("./file/service_no_detail.txt",encoding='utf8')
tech_f = open("./file/comd_no_detail.txt",encoding='utf8')
# #页数
i=1
try:
	tech_content=tech_f.read().split("\n")
	for ele in tech_content:
		ele = ele.lower()
		tech = ele.replace(" ","%20")
		serv_dic[ele]={}
		#url = 'https://so.csdn.net/api/v2/search?q='+tech+'%E6%9C%8D%E5%8A%A1%E6%98%AF%E4%BB%80%E4%B9%88&t=blog&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&platform=pc'
		url2 = 'https://so.csdn.net/api/v2/search?q='+tech+'%E5%91%BD%E4%BB%A4%E6%98%AF%E4%BB%80%E4%B9%88&t=blog&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&platform=pc'
		print(url2)
		get_article_url2(url2,ele,serv_dic)
		logger.critical(ele+":::"+str(serv_dic[ele]))
		logger.critical("分界线")
finally:
	tech_f.close()