# encoding=utf8

#用于统一命令参数格式(linux)

from py2neo import Graph,Node,Relationship

graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

com_node = graph.nodes.match("命令",platform='linux')

for ele in com_node:
	parameter = ele['parameter']
	# print(ele)
	if parameter:
		parameter2 = str(parameter).replace('/','|||')
		ele.update({'parameter':parameter2})
		graph.push(ele)