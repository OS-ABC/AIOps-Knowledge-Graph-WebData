# encoding=utf8
#准备计算服务与命令关系的评价
#准确率、召回率、F值
import copy
f=open("./file/serv_dic.txt","r+")
f2=open("./file/service_comd_test.txt","r+")

cor_list=[]
ret_list=[]
f1_list=[]

try:
	content = eval(f.read())
	content2 = copy.deepcopy(content)
	test = eval(f2.read())
	keng = 1 #阈值
	while keng < 10:
		out = 0 #提取出来的信息条数
		for ele in content:
			if content[ele]:
				for com in content[ele]:
					content[ele][com] = content[ele][com] - keng
					if content[ele][com] > 0:
						out = out + 1
			else:
				out = out + 1

		correct = 0#提取出来的信息正确的条数
		count = 0 #测试样本中信息的条数
		for ele in test:
			if test[ele]:
				for a in test[ele]:
					count = count + 1
			else:
				count = count + 1

		for ele in content:
			if content[ele]:
				for key,val in content[ele].items():
					if val > 0 and key in test[ele]:
						correct = correct + 1
			else:
				if not test[ele]:
					correct = correct + 1
		#准确率：（正确预测信息条数/所有预测信息条数）反映了被分类器判定的正例中真正的正例样本的比重
		cor_per = round(correct*100/out,2)
		#召回率：（正确预测信息条数/所有正确信息条数（一般时测试集条数））反映了被正确判定的正例占总的正例的比重 
		ret_per = round(correct*100/count,2)
		#
		f1_per = round(cor_per*ret_per*2/(cor_per+ret_per),2)
		cor_list.append(cor_per)
		ret_list.append(ret_per)
		f1_list.append(f1_per)
		content = copy.deepcopy(content2)
		keng = keng + 1


	print(cor_list)
	print(ret_list)
	print(f1_list)

	# print(content2)




finally:
	f.close()
	f2.close()