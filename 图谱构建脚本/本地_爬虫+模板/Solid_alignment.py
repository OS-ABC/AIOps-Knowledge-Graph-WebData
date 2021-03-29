# encoding=utf8
from py2neo import Graph,Node,Relationship
from min_edit import edit

graph = Graph("http://localhost:7474",auth=("neo4j","SSPKUsspku12345"))

serv_node = graph.nodes.match("服务")
node_name = graph.run('MATCH (n:`服务`) RETURN n.name').data()
# print(type(node_name))

def my_union(str,name1,name2):
	comd1_name = graph.run('MATCH (n:`服务`)-[]-(m:`'+str+'`) where n.name="'+name1+'" RETURN m.name').data()
	comd2_name = graph.run('MATCH (n:`服务`)-[]-(m:`'+str+'`) where n.name="'+name2+'" RETURN m.name').data()
	unin=0
	for data1 in comd1_name:
		for data2 in comd2_name:
			if data1['m.name'] == data2['m.name']:
				unin = unin + 1
	mylist = []
	mylist.append(unin)
	mylist.append(len(comd1_name)+len(comd2_name))
	return mylist


for i in range(1,len(node_name)):
	if node_name[i] == "服务":
		continue
	for j in range(i+1,len(node_name)):
		if node_name[j] == "服务":
			continue
		name1 = node_name[i]['n.name']
		name2 = node_name[j]['n.name']
		length1 = len(name1)
		length2 = len(name2)
		sum_1 = length1 + length2
		# print(name1)
		abc = (sum_1 - edit(name1,name2))/sum_1

		mylist = my_union('命令',name1,name2)
		if mylist[1] == 0:
			continue
		elif abc*0.5 + 0.5*mylist[0]/mylist[1] > 0.7:
			print(name1+":::"+name2+":::"+str(abc))

