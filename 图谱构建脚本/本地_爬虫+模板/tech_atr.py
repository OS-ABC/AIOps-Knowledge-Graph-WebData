# encoding=utf8
#这个脚本用来爬取服务与配置文件的关系，并对关系个数做统计，结果存入serv_file_dic.txt
#从neo4j中读取服务，用服务名称拼接csdn的url做成爬虫，每个服务爬取800篇博客
#每篇博客用模板识别关系
# from urllib import request
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
# from py2neo import Graph,Node,Relationship

# User_Agent列表
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
]

# 产生一个随机User-Agent
headers ={
    'User-Agent':random.choice(user_agent_list),
    "Access-Control-Allow-Origin":"*",
    'Connection': 'close'
    #'cookie':'uuid_tt_dd=10_9998271520-1602569557550-935264; dc_session_id=10_1602569557550.613995; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_9998271520-1602569557550-935264; dc_sid=e916dd597bb140fd265a26b745941a70; c_first_ref=default; c_first_page=https%3A//so.csdn.net/so/search/s.do%3Fq%3Ddsls%2520%25E5%25AE%2598%25E7%25BD%2591%26t%3Dblog%26o%3D%26s%3D%26tm%3D%26v%3D%26l%3D%26lv%3D%26u%3D%26ft%3D; c_segment=0; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1604906105,1604909184,1604909362,1607070179; announcement-new=%7B%22isLogin%22%3Afalse%2C%22announcementUrl%22%3A%22https%3A%2F%2Flive.csdn.net%2Froom%2Fweixin_47115905%2FbcobcpkN%3Futm_source%3Dgonggao_1201%22%2C%22announcementCount%22%3A0%2C%22announcementExpire%22%3A3600000%7D; unlogin_scroll_step=1607070202102; SESSION=d3635b2a-0826-4570-8187-ce2dced8ee26; c_utm_medium=distribute.pc_search_result.none-task-blog-2%7Eblog%7Efirst_rank_v1%7Erank_blog_v1-2-87995129.pc_v1_rank_blog_v1; c_utm_term=dsls%20%E5%AE%98%E7%BD%91; c_page_id=default; __gads=ID=e4afec359d81ab44-22b80f50fac4002f:T=1607070285:RT=1607070285:S=ALNI_MbeCZeTqHTbLQz2qvBMpd5k0z2eeQ; log_Id_click=13; c-login-auto=20; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1607070714; dc_tos=qkt3p7; log_Id_pv=24; log_Id_view=76'
}

proxies={
'http':'127.0.0.1:8080',
'https':'127.0.0.1:8080'
}

#登录neo4j
# graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

#爬取每个命令的详细内容(包含爬虫)
def order_detail(url2,serv,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip):
	response = requests.get(url2,headers=headers)
	# 发送请求
	response2 = BeautifulSoup(response.text, 'html.parser')
	article2 = response2.select('article p')
	# title = response2.select('h1[class="title-article"]')
	# print(title[0].get_text())
	for ele in article2:
		txt = ele.get_text()
		txt = txt.strip().replace("\xa0","")
		txt = txt.lower()
		txt2 = re.split('。|！|？',txt)
		for ele2 in txt2:
			# '功能','版本','创始人','官网','诞生时间'
			if tip == '特性':
				# 功能
				# sys.exit(0)
				print()
				# fun_rule1(url2,ele2,serv,fun_dic)
				# fun_rule2(url2,ele2,serv,fun_dic)
			#版本
			elif tip == '版本':
				# sys.exit(0)
				edtion_rule(url2,ele2,serv,edtion_dic)
				
			elif tip == '创始人':
				# sys.exit(0)
				author_rule(url2,ele2,serv,author_dic)
			elif tip == '官网':
				web_rule(url2,ele2,serv,web_dic)
				# sys.exit(0)
			else:
				sys.exit(0)
				#开发人员
				# born_rule(url2,ele2,serv,author_dic)

			# web_rule(url2,ele2,serv,web_dic)
	response.close()

def get_length(generator):
	if hasattr(generator,"__len__"):
		return len(generator)
	else:
		return sum(1 for _ in generator)

#判断字符串是否是纯英文
def judge_pure_english(keyword):
	if keyword is "" or keyword is None:
		return False
	for ch in keyword:
		#(ord(ch) not in (97,122)) and (ord(ch) not in (65,90)):
		if (ord(ch) < 97 and ord(ch) > 90) or (ord(ch) > 122) or (ord(ch)<65):
			return False
	return True

#处理字符串
def str_sort(txt):
	my_str = []
	file_cont_list=['.','/',' ']
	key = 0
	while key < len(txt) and key >= 0:
		if txt[key] in file_cont_list or judge_pure_english(txt[key]):
			if key-1>=0 and re.search(r'([A-Za-z0-9]|\.|/|\s)*',txt[key-1]).group():
				txt[key-1] = txt[key-1]+txt[key]
				del txt[key]
				key = key - 1
		key = key + 1

# txt1="python2.x与3​​.x版本区别"
# txt1 = txt1.strip().replace("\xa0","")
# seg_list = pseg.cut(txt1)  # 默认是精确模式
# list2 = jieba.cut(txt1)
# # txt = list(seg_list)
# # print(seg_list[-1])
# # for word in seg_list:
# # 	print(word)
# # str_sort(txt)
# # print(type(list2))
# for ele in list2:
# 	print(ele)


#功能模板
def fun_rule1(url,txt1,tech,fun_dic):
	# print(url)
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	# print("：：：：：：：：：：：：：：：：：：：一切ok")
	##########这里是爬取了有关系的代码#############
	# if '服务' in txt and '命令' in txt:
	# 	aa = txt.index('服务')
	# 	bb = txt.index('命令')
	# 	if judge_pure_english(txt[aa-1]) and judge_pure_english(txt[bb-1]):
	# 		print(txt1)
	# return
	##########这里是爬取了又关系的代码#############
	comd_list=['特性','特点','功能']
	verb_list=['具有','具备','包含','引入','提供']
	for ele in comd_list:
		for ele2 in verb_list:
			if tech in txt and ele in txt and ele2 in txt:
				index1 = txt.index(tech)
				index2 = txt.index(ele2)
				index3 = txt.index(ele)
				# print(txt1)
				if index1 < index2 and index2 < index3:
					temp = txt[index2+1:index3]
					res = ""
					if '，' in temp:
						break
					else:
						# print(temp)
						for ele3 in temp:
							if ele3 == '特性':
								index = txt.index(ele)
								if txt[index-1] == '的':
									add2dic(tech,fun_dic,txt[index-2]+txt[index-1]+ele)
								else:
									add2dic(tech,fun_dic,txt[index-1]+ele)
							elif ele3 == '性':
								ind = txt.index(ele)
								add2dic(tech,fun_dic,txt[ind-2]+txt[ind-1]+ele)
							else:
								continue


def fun_rule2(url,txt1,tech,fun_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	if tech in txt:
		for ele in txt:
			if ele == '特性':
				index = txt.index(ele)
				if txt[index-1] == '的':
					add2dic(tech,fun_dic,txt[index-2]+txt[index-1]+ele)
				else:
					add2dic(tech,fun_dic,txt[index-1]+ele)
			elif ele[-1] == '性':
				index = txt.index(ele)
				add2dic(tech,fun_dic,txt[index-1]+ele)
			else:
				continue

def user_rule(url2,ele2,serv,user_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	if "服务" in txt and tech in txt:
		# print("服务：：：："+txt1)
		server_index = txt.index("服务")
		if server_index - 1 >= 0 and judge_pure_english(txt[server_index-1]):
			add2dic(tech,tech_comd_dic,txt[server_index-1])


def editon_sort(txt):
	i = 0
	while i < len(txt) and i > 0:
		if re.match(r'(\.|[a-z]|[0-9]|_|\+)*',txt[i]) and i - 1 >= 0:
			if re.match(r'(\.|[a-z]|[0-9]|_|\+)+',txt[i-1]):
				txt[i-1] = txt[i]+txt[i-1]
			del txt[i]
			i = i -1
		i = i + 1

# txt1="python2.x与3.x版本区别"
# # txt1 = txt1.strip().replace("\xa0","")
# list2 = jieba.cut(txt1)
# a = list(list2)
# editon_sort(a)
# print(",".join(a))

def edtion_rule(url2,txt1,tech,edtion_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	# str_sort(txt)
	editon_sort(txt)
	# if tech in txt:
	# 	index = txt.index(tech)
	# 	if index + 1 < len(txt) and txt[index+1] == " ":
	# 		if re.match(r'(\.|[a-z]|[0-9]|_|\+)+',txt[index+2]):
	# 			print(txt[index+2])
	# if tech in txt and "版本" in txt:
	# 	index = txt.index("版本")
	# 	index2 = txt.index(tech)
	# 	if re.match(r'(\.|[a-z]|[0-9]|_|\+)+',txt[index-1]):
	# 		print(txt1)
	# 		print(txt[index-1])
	# 	if txt[index-1] == ' ' and re.match(r'(\.|[a-z]|[0-9]|_|\+)+',txt[index-2]):
	# 		print(txt1)
	# 		print(txt[index-2])
	# 	if index+1<len(txt) and txt[index+1] == ' ':
	# 		print(txt)
	reg= tech+'(\.|[0-9]|v|_|\+)+'
	for ele in txt:
		if re.match(reg,ele):
			add2dic(tech,edtion_dic,ele)
			# edtion_dic(ele)


def author_rule(url2,txt1,tech,author_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	ner_list=['创始人']
	for ele in ner_list:
		if ele in txt and tech in txt:
			index = txt.index(ele)
			index2 = txt.index(tech)
			# if re.match(r'([a-z]|\s)+',txt[index+1]):
			# 	print(txt[index+1])
			# if index2 == index -1:
			# 	if txt[index+1] == " ":
			# 		print(ele[index+2])
			# 	else:
			# 		print(ele[index+1])

			for ele2 in txt[index:]:
				if ele2 == '，':
					break
				if re.match(r'([a-z]|\s)+',ele2) and ele2.strip() != tech and index > index2:
					# print(index == index2+1)
					# print(txt1)
					# print(ele2)
					add2dic(tech,author_dic,ele2)
					break


def web_rule(url2,txt1,tech,web_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	n_list=['官方网站','官网']
	for ele in n_list:
		if ele in txt and tech in txt:
			web = re.findall(r'(https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])', txt1)
			if web:
				for w in web:
					add2dic(tech,web_dic,w)





#向字典添加元素
def add2dic(serv,tech_dic,commond):
	if commond in tech_dic[serv]:
		tech_dic[serv][commond] = tech_dic[serv][commond] + 1
	else:
		tech_dic[serv][commond] = 1



# order_detail("https://blog.csdn.net/itfantasy/article/details/16330951?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160263745219724839242649%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=160263745219724839242649&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v28-1-16330951.first_rank_ecpm_v3_pc_rank_v2&utm_term=acpid&spm=1018.2118.3001.4187")

#获取每个博客页面的url列表
def get_article_url(url,serv,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text, 'html.parser')
	article = soup.select('div dl a')
	for ele in article:
		article_url=ele['href']
		order_detail(article_url,serv,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip)
	req.close()

def get_article_url2(url,serv,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip):
	req = requests.get(url,headers=headers)
	content = json.loads(req.text)
	for ele in content['result_vos']:
		order_detail(ele['url'],serv,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip)
	req.close()

logging.basicConfig(filename = "./file/tech_atr.log",level = logging.CRITICAL)
logger = logging.getLogger()
#字典：用来存储服务与配置文件的次数关系：{"cron":{"crond":10,"vi":1}}
fun_dic={}
platform_dic={}
user_dic={}

edtion_dic={}
author_dic={}
web_dic={}
tech_f = open("./file/test_tech.txt",encoding='utf8')

# #页数
i=1
try:
	tech_content=tech_f.read().split("\n")
	for ele in tech_content:
		ele = ele.lower()
		tech = ele.replace(" ","%20")
		if tech == "技术":
			continue
		edtion_dic[ele]={}
		author_dic[ele]={}
		web_dic[ele]={}
		atr_list=['版本','创始人','官网']
		for tip in atr_list:
			# url = 'https://so.csdn.net/so/search/s.do?q='+ele+'%20'+tip+'&t=blog&o=&s=&tm=&v=&l=&lv=&u=&ft='
			url = "https://so.csdn.net/api/v2/search?q="+parse.quote(ele)+"+"+parse.quote(tip)+"&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&platform=pc"
			# url = 'https://so.csdn.net/so/search/s.do?q=java%20'+ele+'&t=blog&platform=pc&p=1&s=&tm=&v=&l=&u=&ft='
			print(url)
			get_article_url2(url,ele,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,tip)
		logger.critical(ele+":::"+str(edtion_dic[ele]))
		logger.critical(ele+":::"+str(author_dic[ele]))
		logger.critical(ele+":::"+str(web_dic[ele]))
		logger.critical("分界线")
finally:
	tech_f.close()


# service='cron'
# fun_dic[service]={}
# url = 'https://so.csdn.net/so/search/s.do?q='+service+'服务&t=blog&platform=pc&p=4&s=&tm=&v=&l=&u=&ft='
# get_article_url(url,ele,fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic)




# edtion_dic['java']={}
# author_dic['java']={}
# web_dic['java']={}
# # fun_dic['css']={}
# # atr_list=['版本','创始人','官网','诞生时间']
# atr_list=['版本']
# for ele in atr_list:
# 	# url = 'https://so.csdn.net/so/search/s.do?q=java%20'+ele+'&t=blog&o=&s=&tm=&v=&l=&lv=&u=&ft='
# 	a = "java"
# 	url = "https://so.csdn.net/api/v2/search?q="+parse.quote(a)+"+"+parse.quote(ele)+"&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&platform=pc"
# 	# url = 'https://so.csdn.net/so/search/s.do?q=java%20'+ele+'&t=blog&platform=pc&p=1&s=&tm=&v=&l=&u=&ft='
# 	# str2 = parse.quote(url)
# 	print(url)
# 	# print(url)
# 	get_article_url2(url,'java',fun_dic,user_dic,edtion_dic,platform_dic,author_dic,web_dic,ele)

# print(edtion_dic)
# print(web_dic)
# print(author_dic)






# logger.critical('java'+":::"+str(tech_comd_dic['java']))
# logger.critical('java'+":::"+str(tech_server_dic['java']))
# logger.critical('java'+":::"+str(tech_file_dic['java']))
# logger.critical("")
# print('java'+" "+str(tech_comd_dic['java']),file=f1)
# print('java'+" "+str(tech_server_dic['java']),file=f2)
# print('java'+" "+str(tech_file_dic['java']),file=f3)

