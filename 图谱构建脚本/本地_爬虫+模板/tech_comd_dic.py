# encoding=utf8
#这个脚本用来爬取技术与配置文件的关系，并对关系个数做统计，结果存入serv_file_dic.txt
#从neo4j中读取服务，用服务名称拼接csdn的url做成爬虫，每个服务爬取800篇博客
#每篇博客用模板识别关系
# from urllib import request
import urllib.request
import requests
import random
import jieba
import re
import logging
from bs4 import BeautifulSoup
import jieba.posseg as pseg
# from py2neo import Graph,Node,Relationship
jieba.add_word("配置信息", freq=5, tag='n')
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

proxies={
'http':'127.0.0.1:8080',
'https':'127.0.0.1:8080'
}

#登录neo4j
# graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

#爬取每个命令的详细内容(包含爬虫)
def order_detail(url2,serv,tech_comd_dic,tech_server_dic,tech_file_dic):
	response = requests.get(url2,headers=headers)
	# 发送请求
	response2 = BeautifulSoup(response.text, 'html.parser')
	article2 = response2.select('article p')
	for ele in article2:
		txt = ele.get_text()
		txt = txt.strip().replace("\xa0","")
		txt = txt.lower()
		txt2 = re.split('。|！|？',txt)
		for ele2 in txt2:
			# 采用摸版1
			tech_command_rule1(url2,ele2,serv,tech_comd_dic)
			# 采用模板2
			tech_server_rule(url2,ele2,serv,tech_server_dic)
			# 
			tech_file_rule(url2,ele2,serv,tech_file_dic)
	response.close()

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

# txt1="apache mysql的配置文件在这里cd /etc/bin/my.ini."
# txt1 = txt1.strip().replace("\xa0","")
# seg_list = jieba.cut(txt1)  # 默认是精确模式
# txt = list(seg_list)
# str_sort(txt)
# print(txt)

# #模板1：<tech><verb><comd>
# def tech_command_rule1(url,txt1,tech,tech_comd_dic):
# 	# print(url)
# 	seg_list = jieba.cut(txt1)  # 默认是精确模式
# 	txt = list(seg_list)
# 	str_sort(txt)
# 	# print("：：：：：：：：：：：：：：：：：：：一切ok")
# 	##########这里是爬取了有关系的代码#############
# 	# if '服务' in txt and '命令' in txt:
# 	# 	aa = txt.index('服务')
# 	# 	bb = txt.index('命令')
# 	# 	if judge_pure_english(txt[aa-1]) and judge_pure_english(txt[bb-1]):
# 	# 		print(txt1)
# 	# return
# 	##########这里是爬取了又关系的代码#############
# 	if "命令" in txt and tech in txt:
# 		comd_index = txt.index("命令")
# 		if comd_index - 1>=0 and judge_pure_english(txt[comd_index-1]):
# 			# print()
# 			add2dic(tech,tech_comd_dic,txt[comd_index-1])


# def tech_server_rule(url,txt1,tech,tech_comd_dic):
# 	seg_list = jieba.cut(txt1)  # 默认是精确模式
# 	txt = list(seg_list)
# 	str_sort(txt)
# 	if "服务" in txt and tech in txt:
# 		# print("服务：：：："+txt1)
# 		server_index = txt.index("服务")
# 		if server_index - 1 >= 0 and judge_pure_english(txt[server_index-1]):
# 			add2dic(tech,tech_comd_dic,txt[server_index-1])


# def tech_file_rule(url,txt1,tech,tech_file_dic):
# 	seg_list = jieba.cut(txt1)  # 默认是精确模式
# 	txt = list(seg_list)
# 	str_sort(txt)
# 	if "配置文件" in txt and tech in txt:
# 		# print("配置文件：：：："+txt1)
# 		for ele in txt:
# 			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
# 				add2dic(tech,tech_file_dic,ele)
# 				# print(ele)

def verb_config(first_index,second_index,alist,verb_list):
	mylist = alist[first_index+1:second_index]
	dot=['。','！','；','？']
	s = 'a'
	for w in mylist:
		if w in dot:
			return False
		s = s+ w
	s = s +'b'
	words = pseg.cut(s)
	for word,flag in words:
		if word in verb_list or flag == 'v':
			return True

#模板1：<tech><verb><comd>
def tech_command_rule1(url,txt1,tech,tech_comd_dic):
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
	# if "命令" in txt and tech in txt:
	# 	comd_index = txt.index("命令")
	# 	if comd_index - 1>=0 and judge_pure_english(txt[comd_index-1]):
	# 		# print()
	# 		add2dic(tech,tech_comd_dic,txt[comd_index-1])
	verb_list=['是','使用','运用','执行','通过','利用','用']
	verb_list2=['是','属于']
	if tech in txt and ("命令" in txt or "指令" in txt):
		tech_index = txt.index(tech)
		if "命令" in txt:
			comd_index = txt.index("命令")
		elif "指令" in txt:
			comd_index = txt.index("指令")
		if comd_index - 1>=0 and judge_pure_english(txt[comd_index-1]):
			if tech_index > comd_index:
				res = verb_config(comd_index,tech_index,txt,verb_list2)
				print("============与命令1")
				if res:
					add2dic(tech,tech_comd_dic,txt[comd_index-1])
					# print("txt1")
			elif comd_index > tech_index:
				# print("txt1")
				print("============与命令2")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_comd_dic,txt[comd_index-1])
		elif comd_index + 1<len(txt) and judge_pure_english(txt[comd_index+1]):
			if tech_index > comd_index:
				print("============与命令3")
				res = verb_config(comd_index,tech_index,txt,verb_list2)
				if res:
					add2dic(tech,tech_comd_dic,txt[comd_index+1])
					# print("txt1")
			elif comd_index > tech_index:
				print("txt1")
				print("============与命令4")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_comd_dic,txt[comd_index+1])
		elif comd_index + 2<len(txt) and judge_pure_english(txt[comd_index+2]):
			if tech_index > comd_index:
				res = verb_config(comd_index,tech_index,txt,verb_list2)
				print("============与命令5")
				if res:
					add2dic(tech,tech_comd_dic,txt[comd_index+1])
					# print("txt1")
			elif comd_index > tech_index:
				print("txt1")
				print("============与命令6")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_comd_dic,txt[comd_index+1])
	elif tech in txt and("输入" in txt or "键入" in txt):
		tech_index = txt.index(tech)
		if "输入" in txt:
			verb_index = txt.index("输入")
		elif "键入" in txt:
			verb_index = txt.index("键入")
		if verb_index + 1<len(txt) and judge_pure_english(txt[verb_index+1]):
			if tech_index > verb_index+1:
				res = verb_config(verb_index+1,tech_index,txt,verb_list)
				print("============与命令7")
				if res:
					add2dic(tech,tech_comd_dic,txt[verb_index+1])
					
					# print("txt1")
			elif verb_index+1 > tech_index:
				print("txt1")
				print("============与命令8")
				res = verb_config(tech_index,verb_index+1,txt,verb_list2)
				if res:
					# print("txt1")
					add2dic(tech,tech_comd_dic,txt[verb_index+1])



def tech_server_rule(url,txt1,tech,tech_comd_dic):
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	# if "服务" in txt and tech in txt:
	# 	# print("服务：：：："+txt1)
	# 	server_index = txt.index("服务")
	# 	if server_index - 1 >= 0 and judge_pure_english(txt[server_index-1]):
	# 		add2dic(tech,tech_comd_dic,txt[server_index-1])
	verb_list=['是','使用','运用','通过','利用','用','执行','包含']
	verb_list2=['是','属于','服务']
	if tech in txt and "服务" in txt:
		tech_index = txt.index(tech)
		serv_index = txt.index("服务")
		if serv_index - 1>=0 and judge_pure_english(txt[serv_index-1]):
			if tech_index > serv_index:
				print("============与服务1")
				res = verb_config(serv_index,tech_index,txt,verb_list2)
				if res:
					add2dic(tech,tech_server_dic,txt[serv_index-1])
					# print("txt1")
			elif serv_index > tech_index:
				# print("txt1")
				print("============与服务2")
				res = verb_config(tech_index,serv_index,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_server_dic,txt[serv_index-1])
		elif serv_index + 1<len(txt) and judge_pure_english(txt[serv_index+1]):
			if tech_index > serv_index+1:
				res = verb_config(serv_index+1,tech_index,txt,verb_list2)
				print("============与服务3")
				if res:
					add2dic(tech,tech_server_dic,txt[serv_index+1])
					# print("txt1")
			elif serv_index+1 > tech_index:
				print("============与服务4")
				res = verb_config(tech_index,serv_index+1,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_server_dic,txt[serv_index+1])
		elif serv_index + 2<len(txt) and judge_pure_english(txt[serv_index+2]):
			if tech_index > serv_index:
				res = verb_config(serv_index+2,tech_index,txt,verb_list2)
				print("============与服务5")
				if res:
					add2dic(tech,tech_server_dic,txt[serv_index+2])
					# print("txt1")
			elif serv_index+2 > tech_index:
				print("============与服务6")
				# print("txt1")
				
				res = verb_config(tech_index,serv_index+2,txt,verb_list)
				if res:
					print("txt1")
					add2dic(tech,tech_server_dic,txt[serv_index+2])
	elif tech in txt and("启动" in txt or "关闭" in txt or "停止" in txt or "查看" in txt):
		tech_index = txt.index(tech)
		if "启动" in txt:
			verb_index = txt.index("启动")
		elif "关闭" in txt:
			verb_index = txt.index("关闭")
		elif "停止" in txt:
			verb_index = txt.index("停止")
		elif "查看" in txt:
			verb_index = txt.index("查看")
		if verb_index + 1<len(txt) and judge_pure_english(txt[verb_index+1]):
			if tech_index > verb_index:
				res = verb_config(verb_index,tech_index,txt,verb_list2)
				print("============与服务7")
				if res:
					add2dic(tech,tech_server_dic,txt[verb_index+1])
					# print("txt1")
			elif verb_index > tech_index:
				print("txt1")
				print("============与服务8")
				res = verb_config(tech_index,verb_index,txt,verb_list)
				if res:
					# print("txt1")
					add2dic(tech,tech_server_dic,txt[verb_index+1])


def tech_file_rule(url,txt1,tech,tech_file_dic):
	verb_list=['是','使用','运用','执行','通过','利用','用','包含','配置']
	verb_list2=['是','属于']
	seg_list = jieba.cut(txt1)  # 默认是精确模式
	txt = list(seg_list)
	str_sort(txt)
	# if "配置文件" in txt and tech in txt:
	# 	# print("配置文件：：：："+txt1)
	# 	for ele in txt:
	# 		if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
	# 			# add2dic(tech,tech_file_dic,ele)
	# 			# print(ele)
	if tech in txt and ("配置文件" in txt or "文件" in txt or "配置信息" in txt):
		tech_index = txt.index(tech)
		if "配置文件" in txt:
			file_index = txt.index("配置文件")
		elif "配置信息" in txt:
			file_index = txt.index("配置信息")
		elif "文件" in txt:
			file_index = txt.index("文件")
		for ele in txt[file_index:]:
			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
				target_index = txt.index(ele)
				# print(target_index)
				if tech_index > target_index:
					print("============与配置文件1")
					res = verb_config(target_index,tech_index,txt,verb_list2)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						
				elif target_index > tech_index:
					print("============与配置文件2")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						
		# print("a")
		for ele in reversed(txt[0:file_index]):
			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
				target_index = txt.index(ele)
				if tech_index > target_index:
					print("============与配置文件3")
					res = verb_config(target_index,tech_index,txt,verb_list2)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						
				elif target_index > tech_index:
					print("============与配置文件4")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						
	elif tech in txt and ("配置" in txt or "修改" in txt):
		tech_index = txt.index(tech)
		if "配置" in txt:
			file_index = txt.index("配置")
		elif "修改" in txt:
			file_index = txt.index("修改")
		for ele in txt[file_index:]:
			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
				target_index = txt.index(ele)
				if tech_index > target_index:
					print("============与配置文件5")
					res = verb_config(target_index,tech_index,txt,verb_list2)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						break
				elif target_index > tech_index:
					print("============与配置文件6")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						# print("txt1")
						add2dic(tech,tech_file_dic,ele)
						break

#向字典添加元素
def add2dic(serv,tech_dic,commond):
	if commond in tech_dic[serv]:
		tech_dic[serv][commond] = tech_dic[serv][commond] + 1
	else:
		tech_dic[serv][commond] = 1



# order_detail("https://blog.csdn.net/itfantasy/article/details/16330951?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522160263745219724839242649%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=160263745219724839242649&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_v2~rank_v28-1-16330951.first_rank_ecpm_v3_pc_rank_v2&utm_term=acpid&spm=1018.2118.3001.4187")

#获取每个博客页面的url列表
def get_article_url(url,serv,tech_comd_dic,tech_server_dic,tech_file_dic):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.text, 'html.parser')
	article = soup.select('div dl a')
	for ele in article:
		article_url=ele['href']
		order_detail(article_url,serv,tech_comd_dic,tech_server_dic,tech_file_dic)
	req.close()

logging.basicConfig(filename = "./file/server.log",level = logging.CRITICAL)
logger = logging.getLogger()
#字典：用来存储服务与配置文件的次数关系：{"cron":{"crond":10,"vi":1}}
tech_comd_dic={}
tech_server_dic={}
tech_file_dic={}
tech_f = open("./file/technolony.txt",encoding='utf8')
# f1=open("./file/tech_comd_dic2.txt","r+",encoding='utf8')
# f2=open("./file/tech_server_dic.txt","r+",encoding='utf8')
# f3=open("./file/tech_file_dic.txt","r+",encoding='utf8')
# #页数
i=1
try:
	# serv_node = graph.nodes.match("技术")
	tech_content=tech_f.read().split("\n")
	for ele in tech_content:
		ele = ele.lower()
		tech = ele.replace(" ","%20")
		tech_comd_dic[ele]={}
		tech_server_dic[ele]={}
		tech_file_dic[ele]={}
		while i < 10:
			url = 'https://so.csdn.net/so/search/s.do?q='+tech+'&t=blog&platform=pc&p='+str(i)+'&s=&tm=&v=&l=&u=&ft='
			print(url)
			get_article_url(url,ele,tech_comd_dic,tech_server_dic,tech_file_dic)
			i = i + 1
		i = 1
		logger.critical(ele+":::"+str(tech_comd_dic[ele]))
		logger.critical(ele+":::"+str(tech_server_dic[ele]))
		logger.critical(ele+":::"+str(tech_file_dic[ele]))
		logger.critical("分界线")
		# print(ele+" "+str(tech_comd_dic[ele]),file=f1)
		# print(ele+" "+str(tech_server_dic[ele]),file=f2)
		# print(ele+" "+str(tech_file_dic[ele]),file=f3)
finally:
	# tech_f.close()

	# try:
	# 	f1.write(str(tech_comd_dic))
	# 	f2.write(str(tech_server_dic))
	# 	f3.write(str(tech_file_dic))
	# 	print(tech_comd_dic)
	# 	print(tech_server_dic)
	# 	print(tech_file_dic)
	# finally:
	tech_f.close()
	# f1.close()
	# f2.close()
	# f3.close()


# service='cron'
# tech_comd_dic[service]={}
# url = 'https://so.csdn.net/so/search/s.do?q='+service+'服务&t=blog&platform=pc&p=4&s=&tm=&v=&l=&u=&ft='
# get_article_url(url,service,tech_comd_dic,tech_server_dic,tech_file_dic)

# tech_comd_dic['java']={}
# tech_server_dic['java']={}
# tech_file_dic['java']={}
# while i < 20:
# 	url = 'https://so.csdn.net/so/search/s.do?q=java&t=blog&platform=pc&p='+str(i)+'&s=&tm=&v=&l=&u=&ft='
# 	print(url)
# 	get_article_url(url,'java',tech_comd_dic,tech_server_dic,tech_file_dic)
# 	i = i + 1
# # print(tech_comd_dic)
# # print(tech_server_dic)
# # print(tech_file_dic)
# logger.critical('java'+":::"+str(tech_comd_dic['java']))
# logger.critical('java'+":::"+str(tech_server_dic['java']))
# logger.critical('java'+":::"+str(tech_file_dic['java']))
# logger.critical("")
# # print('java'+" "+str(tech_comd_dic['java']),file=f1)
# # print('java'+" "+str(tech_server_dic['java']),file=f2)
# # print('java'+" "+str(tech_file_dic['java']),file=f3)
# tech_f.close()
# f1.close()
# f2.close()
# f3.close()
