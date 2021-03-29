# encoding=utf8
#这个脚本用来爬取命令与服务的关系，并对关系个数做统计，结果存入serv_dic.txt
#从neo4j中读取服务，用服务名称拼接csdn的url做成爬虫，每个服务爬取800篇博客
#每篇博客用模板识别关系
from urllib import request
from urllib.request import build_opener,ProxyHandler
import requests
import random
import jieba
import re
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship
import jieba.posseg as posseg

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



#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

#爬取每个命令的详细内容(包含爬虫)
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
			server_command_rule1(url2,ele2,serv,serv_dic)
			#采用模板2
			server_command_rule2(url2,ele2,serv,serv_dic)

#判断字符串是否是纯英文
def judge_pure_english(keyword):
	if keyword is "" or keyword is None:
		return False
	for ch in keyword:
		#(ord(ch) not in (97,122)) and (ord(ch) not in (65,90)):
		if (ord(ch) < 97 and ord(ch) > 90) or (ord(ch) > 122) or (ord(ch)<65):
			return False
	return True


#模板1：<service><verb><command>
#....服务.....'使用'|'运用'|'执行'|'通过'|'利用'|'用'(XXX命令|命令XXX)....
def server_command_rule1(url,txt1,serv,serv_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	# seg_list2 = posseg.cut(txt1)
	# txt2 = list(seg_list2)
	txt = list(seg_list)
	##########这里是爬取了又关系的代码#############
	# if '服务' in txt and '命令' in txt:
	# 	aa = txt.index('服务')
	# 	bb = txt.index('命令')
	# 	if judge_pure_english(txt[aa-1]) and judge_pure_english(txt[bb-1]):
	# 		print(txt1)
	# return
	##########这里是爬取了又关系的代码#############
	verb_list=['使用','运用','执行','通过','利用','用']
	for ele in verb_list:
		if ele in txt and serv in txt and '命令' in txt:
			verb_index = txt.index(ele)
			service_index = txt.index(serv)
			command_index = txt.index('命令')
			#XXX服务....使用.....XXX命令
			if command_index-1>=0 and service_index < verb_index and command_index > verb_index:
				if judge_pure_english(txt[command_index-1]):
					command_node = graph.nodes.match("命令",name=str(txt[command_index-1])).first()
						# print(command_node)
					if command_node is None:
						continue
					else:
						add2dic(serv,serv_dic,txt[command_index-1])
						print(serv+":::"+txt[command_index-1])
			#XXX服务....使用.....命令XXX
			if command_index+1<len(txt) and service_index < verb_index and command_index > verb_index:
				if judge_pure_english(txt[command_index+1]):
					command_node = graph.nodes.match("命令",name=str(txt[command_index+1])).first()
						# print(command_node)
					if command_node is None:
						continue
					else:
						add2dic(serv,serv_dic,txt[command_index+1])
						print(serv+":::"+txt[command_index+1])

#模板2：<verb><command><service>
#....'使用'|'运用'|'执行'|'通过'|'利用'|'用'(XXX命令|命令XXX)....服务
def server_command_rule2(url,txt1,serv,serv_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	verb_list=['使用','运用','执行','通过','利用','用']
	for ele in verb_list:
		if ele in txt and serv in txt and '命令' in txt:
			verb_index = txt.index(ele)
			service_index = txt.index(serv)
			command_index = txt.index('命令')
			if service_index > command_index and command_index > service_index:
				#通过XXX命令...XXX服务
				if command_index-1>=0 and judge_pure_english(txt[command_index-1]):
					command_node = graph.nodes.match("命令",name=str(txt[command_index-1])).first()
						# print(command_node)
					if command_node is None:
						continue
					else:
						add2dic(serv,serv_dic,txt[command_index-1])
						print(serv+":::"+txt[command_index-1])
				#通过命令XXX...服务
				if command_index+1<len(txt) and judge_pure_english(txt[command_index+1]):
					command_node = graph.nodes.match("命令",name=str(txt[command_index+1])).first()
						# print(command_node)
					if command_node is None:
						continue
					else:
						add2dic(serv,serv_dic,txt[command_index+1])
						print(serv+":::"+txt[command_index+1])
#向字典添加元素
def add2dic(serv,serv_dic,commond):
	if commond in serv_dic[serv]:
		serv_dic[serv][commond] = serv_dic[serv][commond] + 1
	else:
		serv_dic[serv][commond] = 1



# order_detail("https://blog.csdn.net/itfantasy/article/details/16330951?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160263745219724839242649%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=160263745219724839242649&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v28-1-16330951.first_rank_ecpm_v3_pc_rank_v2&utm_term=acpid&spm=1018.2118.3001.4187")

#获取每个博客页面的url列表
def get_article_url(url,serv,serv_dic):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text, 'html.parser')
	article = soup.select('div dl a')
	for ele in article:
		article_url=ele['href']
		order_detail(article_url,serv,serv_dic)
	# print(url)


#字典：用来存储服务与爬取命令的次数关系：{"cron":{"crond":10,"vi":1}}
serv_dic={}
#页数
i=1
try:
	serv_node = graph.nodes.match("服务")
	for ele in serv_node:
		service = ele["name"]
		if service == "服务":
			continue
		# print(service)
		serv_dic[service]={}
		while i < 10:
			url = 'https://so.csdn.net/so/search/s.do?q='+service+'服务&t=blog&platform=pc&p='+str(i)+'&s=&tm=&v=&l=&u=&ft='
			print(url)
			get_article_url(url,service,serv_dic)
			i = i + 1
		i = 1
finally:
	f=open("./serv_dic.txt","r+")
	try:
		# content = f.read()
		# print(eval(content))
		f.write(str(serv_dic))
	finally:
		f.close()
# service='readahead_early'
# serv_dic[service]={}
# url = 'https://so.csdn.net/so/search/s.do?q='+service+'服务&t=blog&platform=pc&p=4&s=&tm=&v=&l=&u=&ft='
# get_article_url(url,service,serv_dic)

# serv_dic['cron']={}
# while i < 20:
# 	url = 'https://so.csdn.net/so/search/s.do?q=cron服务&t=blog&platform=pc&p='+str(i)+'&s=&tm=&v=&l=&u=&ft='
# 	get_article_url(url,'cron',serv_dic)
# 	i = i + 1
# print(serv_dic)
