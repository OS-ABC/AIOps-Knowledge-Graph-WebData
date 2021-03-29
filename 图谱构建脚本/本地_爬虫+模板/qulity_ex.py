# encoding=utf8
from urllib import request
from urllib.request import build_opener,ProxyHandler
from bs4 import BeautifulSoup
import requests
import random
import jieba
import jieba.analyse


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
    "Access-Control-Allow-Origin":"*",
    'Connection': 'close'
}

def get_article_url(url,ele,dic):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text, 'html.parser')
	index = soup.select('span[class="sorryTxt"]')
	if index:
		# print(index[0].get_text())
		return 1
	article = soup.select('div[class="para"]')
	content = ""
	for ele in article:
		content = content + ele.get_text().strip()
	tags = jieba.analyse.extract_tags(content,allowPOS=('ns', 'n', 'vn'),topK=50)
	tags2 = jieba.analyse.textrank(content, topK=50, allowPOS=('ns', 'n', 'vn'))
	res = list(set(tags).intersection(set(tags2)))
	# print(type(tags))
	for ele in res:
		add2dic(ele,dic)
	# print(",".join(tags))

def add2dic(tag,dic):
	if tag in dic:
		dic[tag] = dic[tag] + 1
	else:
		dic[tag] = 1


f = open("./file/technology2.txt",encoding='utf8')
i = 1
dic={}
try:
	content=f.read().split("\n")
	for ele in content:
		if i < 500:
			ele = ele.lower()
			tech = ele.replace(" ","%20")
			url = 'https://baike.baidu.com/item/'+tech
			a = get_article_url(url,ele,dic)
			if a == 1:
				continue
			else:
				i = i + 1
		else:
			break
finally:
	f.close()
	for w in sorted(dic, key=dic.get, reverse=True):
		print (w+":::"+str(dic[w]))
# get_article_url('https://baike.baidu.com/item/Incremental%20data%20warehousing','java',dic)
# get_article_url('https://baike.baidu.com/item/java','java',dic)
# print(dic)
