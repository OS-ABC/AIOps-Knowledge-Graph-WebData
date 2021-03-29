# encoding=utf8
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship

#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

# a = Node("root", name="运维知识")
# a = graph.nodes.match("root",name="运维知识").first()
# # b1 = Node("命令", name="命令")
# # ab1 = Relationship(a, "包含", b1)
# # graph.create(ab1)

# b2 = Node("服务", name="服务")
# ab2 = Relationship(a, "包含", b2)
# graph.create(ab2)

root_node = graph.nodes.match("服务",name="服务").first()
f=open("./service.txt","r",encoding="utf8")
try:
	for line in f.readlines():
		ele = line.split('\t')
		order_node=Node("服务", name=ele[0], detail=ele[1],platform="linux")
		ab = Relationship(root_node, "包含服务", order_node)
		graph.create(ab)
finally:
	f.close()