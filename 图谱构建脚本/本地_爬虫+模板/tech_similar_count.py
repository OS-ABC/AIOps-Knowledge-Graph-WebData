# encoding=utf8
f=open("./file/tech_atr123.txt",encoding="utf8")
res={}
try:
	content = f.read()
	con_list = content.split('\n')
	for num,ele in enumerate(con_list):
		if num%4 == 0:
			edition = eval(ele)
			ed_key = list(edition.keys())[0]
			ed_val = edition[ed_key]
			ed_val_key = list(ed_val.keys())
			ed_strs=""
			for ele in ed_val_key:
				ed_strs = ed_strs + ele +','
			# print("版本："+ed_strs)
			res[ed_key] = {}
			res[ed_key]['版本']=ed_strs
		elif num%4 == 1:
			person = eval(ele)
			per_key = list(person.keys())[0]
			per_val = person[per_key]
			per_val_key = list(per_val.keys())
			per_strs=""
			for ele in per_val_key:
				per_strs = per_strs + ele +','
			# print("创始人："+per_strs)
			res[ed_key]['创始人']=per_strs
		elif num%4 == 2:
			web = eval(ele)
			web_key = list(web.keys())[0]
			web_val = web[web_key]
			web_val_key = list(web_val.keys())
			web_strs=""
			for ele in web_val_key:
				web_strs = web_strs + ele +','
			# print("官网："+web_strs)
			res[ed_key]['官网']=web_strs
		elif num%4 == 3:
			continue
			# print("==============")
		# element = eval(ele)
	print(str(res))
finally:
	f.close()