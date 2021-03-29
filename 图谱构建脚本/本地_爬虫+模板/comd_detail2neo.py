# encoding=utf8
from py2neo import Graph,Node,Relationship

#把命令的介绍录入neo4j

f=open("./file/comd_detail.txt","r",encoding='utf8')

#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","SSPKUsspku12345"))

try:
	content = f.read()
	relation_list = content.split('\n')
	# print(len(relation_list))
	i = 0
	for evey_list in relation_list:
		serv_list = evey_list.split(":::")
		name = serv_list[0]
		serv_dic = eval(serv_list[1])
		serv_str = ""
		for k,v in serv_dic.items():
			serv_str = serv_str+k if serv_str=="" else serv_str+"。"+k
		print(serv_str)
		serv_node = graph.nodes.match("命令",name=name).first()
		serv_node['detail'] = serv_str
		graph.push(serv_node)



finally:
	f.close()