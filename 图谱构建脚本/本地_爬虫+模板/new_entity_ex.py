# encoding=utf8
import urllib.request
import requests
import random
import jieba
import jieba.posseg as pseg
import re
import logging
import sys
from bs4 import BeautifulSoup
from urllib import parse
import json
#半自动获取实体模板
user_agent_list = [
    "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
    "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
    "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)"
]

headers ={
	'User-Agent':random.choice(user_agent_list),
	"Access-Control-Allow-Origin":"*",
	'Connection': 'close',
	"refer":''
}
headers2 ={
    'User-Agent':random.choice(user_agent_list),
    "Access-Control-Allow-Origin":"*",
    'Connection': 'close',
    "refer":''
}
jieba.enable_paddle()

def get_article_url(url,serv,tip,dic,dic2):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text, 'html.parser')
	article = soup.select('div dl a')
	for ele in article:
		article_url=ele['href']
		order_detail(article_url,serv,tip,dic,dic2)
	req.close()


def get_article_url2(url,serv,tip,dic,dic2):
	headers['refer']='https://so.csdn.net/so/search/all?q='+parse.quote(serv)+"%20"+parse.quote(tip)+'&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u='
	# headers[":path"]='/api/v2/search?q='+parse.quote(serv)+"%20"+parse.quote(tip)+'&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u='
	req = requests.get(url,headers=headers)
	if req.status_code==200:
		content = json.loads(req.text)
		i = 0
		for ele in content['result_vos']:
			if i < 10 and i < len(content['result_vos']):
				order_detail(ele['url'],serv,tip,dic,dic2)
				i = i + 1
	req.close()

def order_detail(url2,serv,tip,dic,dic2):
	response = requests.get(url2,headers=headers2)
	# print(url2)
	# 发送请求
	if response.status_code==200:
		response2 = BeautifulSoup(response.text, 'html.parser')
		article2 = response2.select('article p')
		# title = response2.select('h1[class="title-article"]')
		# print(title[0].get_text())
		for ele in article2:
			txt = ele.get_text()
			txt = txt.strip().replace("\xa0","")
			txt = txt.lower()
			txt2 = re.split('。|！|？|，|；|\.|,',txt)
			for ele2 in txt2:
				command_ex(url2,ele2,serv,tip,dic,dic2)
	response.close()

def command_ex(url,ele,serv,tip,dic,dic2):
	# ele = ele.replace(' ','')
	words = pseg.cut(ele,use_paddle=True)
	word_list=[]
	flag_list=[]
	for word, flag in words:
		word_list.append(word)
		flag_list.append(flag)
	if tip in word_list and serv in word_list:
		# find_list = re.findall(r"(([a-zA-Z])*?)命令",ele)
		# for a in find_list:
		# 	print(a)
		index1 = word_list.index(tip)
		index2 = word_list.index(serv)
		if index1>index2:
			left = index2
			right = index1
		else:
			right = index2
			left = index1
		sub_list = word_list[left:right+1]
		res = ""
		for i in sub_list:
			if i == serv:
				res = res + '(([a-zA-Z])*?)'
			else:
				res = res + i
		add2dic(res,dic)
	elif serv in word_list:
		index3 = word_list.index(serv)
		temp = 4
		left = index3 - temp if index3 - temp>0 else 0
		right = index3 + temp if index3 + temp < len(word_list) else len(word_list)
		res = ""
		flag = False
		sub_flag = flag_list[left:index3]
		for f in sub_flag:
			if f is 'v':
				flag = True
				break
		if not flag:
			return
		sub_list = word_list[left:right]
		for i in sub_list:
			if i == serv:
				res = res + '(([a-zA-Z])*?)'
			else:
				res = res + i
		add2dic(res,dic2)
		

# txt='什么是ps命令'
# words = pseg.cut(txt,use_paddle=True)
# word_list=[]
# flag_list=[]
# for word, flag in words:
# 	word_list.append(word)
# 	flag_list.append(flag)
# print(word_list[1])
# print(flag_list[1]=='v')





def add2dic(txt,dic):
	if txt in dic:
		dic[txt] = dic[txt] + 1
	else:
		dic[txt] = 1

# txt="什么是ps命令"
# a = "(([a-zA-Z])*?)命令"
# find_list = re.findall(a,txt)
# print(find_list)

write_file = open("./file/command_model.txt",encoding='utf8',mode='w')
write_file2 = open("./file/command_model2.txt",encoding='utf8',mode='w')
read_file = open("./file/commad_test.txt",encoding='utf8',mode='r')
com_model={}
com_model2={}
try:
	atr_list = read_file.read().split("\n")

	# atr_list=['命令']
	for ele in atr_list:
		# url = 'https://so.csdn.net/so/search/s.do?q=java%20'+ele+'&t=blog&o=&s=&tm=&v=&l=&lv=&u=&ft='
		a = "命令"

		url = "https://so.csdn.net/api/v2/search?q="+parse.quote(ele)+"+"+parse.quote(a)+"&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=2&platform=pc"

		# url = 'https://so.csdn.net/so/search/s.do?q=java%20'+ele+'&t=blog&platform=pc&p=1&s=&tm=&v=&l=&u=&ft='
		# str2 = parse.quote(url)
		# url = "https://so.csdn.net/so/search/s.do?t=all&s=&tm=&v=&l=&lv=&u=&q="+parse.quote(ele)+"%20"+parse.quote(a)
		# url="https://so.csdn.net/so/search/all?q="+ele+"%20"+parse.quote(a)+"&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u="
		print(url)
		# print(url)
		get_article_url2(url,ele,a,com_model,com_model2)
finally:
	write_file.write(str(com_model))
	write_file2.write(str(com_model2))
	# print(com_model)
	print(com_model2)
	write_file.close()
	write_file2.close()
	read_file.close()