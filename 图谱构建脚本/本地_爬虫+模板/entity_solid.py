# encoding=utf8
import json
import MySQLdb
from min_edit import edit
db = MySQLdb.connect(host="localhost", user="root", passwd="12345", db="staffjoy_account", charset='utf8' )
# file = open("./file/entity_align/tech_atr_new.txt",encoding='utf8',mode='r')

def jaccard_sim(a, b):
	unions = len(set(a).union(set(b)))
	intersections = len(set(a).intersection(set(b)))
	if unions == 0:
		return 0
	else:
		return 1 * intersections / unions

def mysort(entity1,entity2):
	r = 0
	for i in range(0, len(entity1[0])):
		res = jaccard_sim(entity1[0][i],entity2[0][i])
		r = r + res
	if r/4>0.6:
		print(entity1[0][0]+":::"+entity2[0][0]+":::"+str(r/4))
	r = 0

try:
	# content_list = file.read().split("\n")
	cursor = db.cursor()
	sql0 = "select name from entity"
	cursor.execute(sql0)
	content_list = cursor.fetchall()
	# print(content_list[0][0])
	for i in range(0, len(content_list)):
		sql1 = "select name,author,web,edition from entity where name='"+content_list[i][0]+"'"
		cursor.execute(sql1)
		results1 = cursor.fetchall()
		# name1 = results[0][1]
		# author1 = results[0][2] if results[0][2] else ""
		# web1 = results[0][3] if results[0][3] else ""
		# edition1 = results[0][4] if results[0][4] else ""
		# entity1 = []
		# entity1.append(name1).append(author1).append(web1).append(edition1)
		for j in range(i+1, len(content_list)):
			sql2 = "select name,author,web,edition from entity where name='"+content_list[j][0]+"'"
			cursor.execute(sql2)
			results2 = cursor.fetchall()
			# name2 = results[0][1]
			# author2 = results[0][2] if results[0][2] else ""
			# web2 = results[0][3] if results[0][3] else ""
			# edition2 = results[0][4] if results[0][4] else ""
			# entity2 = []
			# entity2.append(name2).append(author2).append(web2).append(edition2)
			res = mysort(results1,results2)
			# print(res)
	# sql = "select * from entity where name='html'"
	# cursor.execute(sql)
	# results = cursor.fetchall()
	# print(results[0][1])

finally:
	cursor.close()
	db.close()
	# file.close()