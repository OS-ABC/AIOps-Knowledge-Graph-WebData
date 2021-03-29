# encoding=utf8
from py2neo import Graph,Node,Relationship

#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

root_node = graph.nodes.match("服务",name="服务").first()

f=open("./file/windows_serv.txt","r",encoding='utf8')
try:
	content = f.read()
	serv_list = content.split('\n\n')
	# print(serv_list[0])
	for serv in serv_list:
		item = serv.split('\n')
		for ele in item:
			ele2 = ele.split('：')
			print(ele2[0])

finally:
	f.close()