# encoding=utf8
#构造技术概念
from urllib import request
from urllib.request import build_opener,ProxyHandler
import requests
import random
import jieba
import re
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

graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

root_node = graph.nodes.match("技术",name="技术").first()

#爬取每个技术的属性(包含爬虫)
def tech_detail(url,tech_name):
	# print(url2)
	req2 = requests.get(url,headers=headers)
	req2.encoding = 'utf8'
	# 发送请求
	soup2 = BeautifulSoup(req2.text, 'html.parser')
	index = soup2.select('.baikeLogo')
	#创建图谱节点
	node=Node("技术", name=tech_name)
	if not index:
		name = soup2.select('.basic-info dt')
		val = soup2.select('.basic-info dd')
		i = 0
		while i < len(name):
			if name[i].get_text().replace('\xa0',''):
				v = val[i].select('a')
				if v:
					if v[0].get_text().replace('\xa0',''):
						# print(name[i].get_text()+"::"+v[0].get_text())
						node[name[i].get_text().replace('\xa0','')] = v[0].get_text()
					else:
						# print((name[i].get_text()+"::"+val[i].get_text().replace("\n","")))
						node[name[i].get_text().replace('\xa0','')]=val[i].get_text().replace("\n","")
				else:
					node[name[i].get_text().replace('\xa0','')] = val[i].get_text().replace("\n","")
					# print(name[i].get_text()+"::"+str(val[i]))
			i = i + 1
	# print(node)
	ab = Relationship(root_node, "包含技术", node)
	graph.create(ab)

# node = graph.nodes.match("技术",name="java").first()

# if node:
# 	print(node)

# tech_detail("https://baike.baidu.com/item/git","git")
# tech_detail("https://baike.baidu.com/item/mysql","mysql")



f=open("./file/Technologies.txt","r",encoding='utf8')
try:
	content = f.read()
	tech_list = content.split('\n')
	for ele in tech_list:
		ele = ele.strip().lower()

		node = graph.nodes.match("技术",name=ele).first()
		if not node:
			tech_detail("https://baike.baidu.com/item/"+str(ele.replace(" ","%20")),str(ele))

finally:
	f.close()