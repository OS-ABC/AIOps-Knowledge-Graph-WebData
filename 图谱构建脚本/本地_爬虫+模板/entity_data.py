# encoding=utf8
import json
import MySQLdb
#实体属性准备
db = MySQLdb.connect(host="localhost", user="root", passwd="12345", db="staffjoy_account", charset='utf8' )
file = open("./file/entity_align/tech_atr_new.txt",encoding='utf8',mode='r')

def mysort(dic):
	new_dict= sorted(dic.items(), key=lambda d:d[1], reverse = True)
	return new_dict

# dic = {'a':31, 'bc':5, 'c':3, 'asd':4, 'aa':74, 'd':0}
# mydict= sorted(dic.items(), key=lambda d:d[1], reverse = True)
# print(mydict[0][0])



try:
	# print()
	content_list = file.read().split("\n")
	cursor = db.cursor()
	i = 0
	while i < len(content_list):
		edi = ""
		aut = ""
		w = ""
		#name
		keys = list(eval(content_list[i]).keys())
		# print(type(keys))
		name = keys[0]
		#edition
		edition = mysort(eval(content_list[i])[name])
		if edition:
			edi = edition[0][0]
		i = i + 1
		#author
		author = mysort(eval(content_list[i])[name])
		if author:
			aut = author[0][0]
		i = i + 1
		#web
		web = mysort(eval(content_list[i])[name])
		if web:
			w = web[0][0]
		i = i + 2
		sql = "Insert into entity (name,author,web,edition) values ('"+name+"','"+aut+"','"+w+"','"+edi+"')"
		# print(sql)
		cursor.execute(sql)
		# print(edi+"----------"+aut+"----------"+w)

finally:
	db.commit()
	cursor.close()
	db.close()
	file.close()