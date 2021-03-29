# encoding=utf8
from py2neo import Graph,Node,Relationship
#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","SSPKUsspku12345"))

serv_nodes = graph.nodes.match("命令")

for ele in serv_nodes:
	if ele['detail'] is "" or ele["detail"] is None:
		print(ele['name'])
	# print(ele)
