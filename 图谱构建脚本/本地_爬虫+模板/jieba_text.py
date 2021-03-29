# encoding=utf8
import jieba
import jieba.posseg as pseg
import re
import logging




jieba.add_word("配置信息", freq=5, tag='n')
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
					# add2dic(tech,tech_comd_dic,txt[comd_index-1])
					print("txt1")
			elif comd_index > tech_index:
				print("txt1")
				print("============与命令2")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[comd_index-1])
		elif comd_index + 1<len(txt) and judge_pure_english(txt[comd_index+1]):
			if tech_index > comd_index:
				print("============与命令3")
				res = verb_config(comd_index,tech_index,txt,verb_list2)
				if res:
					# add2dic(tech,tech_comd_dic,txt[comd_index+1])
					print("txt1")
			elif comd_index > tech_index:
				print("txt1")
				print("============与命令4")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[comd_index+1])
		elif comd_index + 2<len(txt) and judge_pure_english(txt[comd_index+2]):
			if tech_index > comd_index:
				res = verb_config(comd_index,tech_index,txt,verb_list2)
				print("============与命令5")
				if res:
					# add2dic(tech,tech_comd_dic,txt[comd_index+1])
					print("txt1")
			elif comd_index > tech_index:
				print("txt1")
				print("============与命令6")
				res = verb_config(tech_index,comd_index,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[comd_index+1])
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
					# add2dic(tech,tech_comd_dic,txt[verb_index+1])
					
					print("txt1")
			elif verb_index+1 > tech_index:
				print("txt1")
				print("============与命令8")
				res = verb_config(tech_index,verb_index+1,txt,verb_list2)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[verb_index+1])



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
					# add2dic(tech,tech_comd_dic,txt[serv_index-1])
					print("txt1")
			elif serv_index > tech_index:
				print("txt1")
				print("============与服务2")
				res = verb_config(tech_index,serv_index,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[serv_index-1])
		elif serv_index + 1<len(txt) and judge_pure_english(txt[serv_index+1]):
			if tech_index > serv_index+1:
				res = verb_config(serv_index+1,tech_index,txt,verb_list2)
				print("============与服务3")
				if res:
					# add2dic(tech,tech_comd_dic,txt[serv_index+1])
					print("txt1")
			elif serv_index+1 > tech_index:
				print("============与服务4")
				res = verb_config(tech_index,serv_index+1,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[serv_index+1])
		elif serv_index + 2<len(txt) and judge_pure_english(txt[serv_index+2]):
			if tech_index > serv_index:
				res = verb_config(serv_index+2,tech_index,txt,verb_list2)
				print("============与服务5")
				if res:
					# add2dic(tech,tech_comd_dic,txt[serv_index+2])
					print("txt1")
			elif serv_index+2 > tech_index:
				print("============与服务6")
				print("txt1")
				
				res = verb_config(tech_index,serv_index+2,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[serv_index+2])
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
					# add2dic(tech,tech_comd_dic,txt[verb_index+1])
					print("txt1")
			elif verb_index > tech_index:
				print("txt1")
				print("============与服务8")
				res = verb_config(tech_index,verb_index,txt,verb_list)
				if res:
					print("txt1")
					# add2dic(tech,tech_comd_dic,txt[verb_index+1])


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
		for ele in txt[file_index:]:
			file_index = txt.index("文件")
			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
				target_index = txt.index(ele)
				print(target_index)
				if tech_index > target_index:
					print("============与配置文件1")
					res = verb_config(target_index,tech_index,txt,verb_list2)
					if res:
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						
				elif target_index > tech_index:
					print("============与配置文件2")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						
		# print("a")
		for ele in reversed(txt[0:file_index]):
			if re.match(r'/([A-Za-z0-9]|\.|/)*',ele):
				target_index = txt.index(ele)
				if tech_index > target_index:
					print("============与配置文件3")
					res = verb_config(target_index,tech_index,txt,verb_list2)
					if res:
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						
				elif target_index > tech_index:
					print("============与配置文件4")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						
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
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						break
				elif target_index > tech_index:
					print("============与配置文件6")
					res = verb_config(tech_index,target_index,txt,verb_list)
					if res:
						print("txt1")
						# add2dic(tech,tech_file_dic,ele)
						break
dic={}
txt=""
# tech_command_rule1("",txt,"ssh",dic)
# tech_server_rule("",txt,"ssh",dic)
tech_file_rule("",txt,"ssh",dic)

# print(re.match(r'([A-Za-z0-9]|\.)*',"ssh0.xml"))