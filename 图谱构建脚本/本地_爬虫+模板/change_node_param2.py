# encoding=utf8

#用于统一命令参数格式(hadoop)

from py2neo import Graph,Node,Relationship

graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

com_node = graph.nodes.match("命令",platform='hadoop')

for ele in com_node:
	parameter = ele['parameter']
	if parameter:
		parameter2 = str(parameter).replace('| ','||| ')
		print(parameter2)
		ele.update({'parameter':parameter2})
		graph.push(ele)