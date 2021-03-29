# encoding=utf8
f=open("./serv_file_dic.txt","r+")
out = 0
try:
	content = eval(f.read())
	for ele in content:
		if content[ele]:
			for com in content[ele]:
				out = out + 1
		else:
			out = out + 1
finally:
	f.close()
	print(out)
