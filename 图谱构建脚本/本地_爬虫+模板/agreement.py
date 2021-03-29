# encoding=utf8
import csv
from py2neo import Graph,Node,Relationship

#把协议实体写入neo4j

f = csv.reader(open('./file/agreement.csv','r'))
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))
root_node = graph.nodes.match("协议",name="协议").first()
ser_node = graph.nodes.match("服务",name="服务").first()

try:
	for i in f:
		name = i[0]
		detail = i[1]
		node=Node("协议", name=name, detail=detail)
		ab = Relationship(root_node, "包含协议", node)
		graph.create(ab)
		if i[2]:
			# print(i[2])
			service = graph.nodes.match("服务",name=i[2]).first()
			if service:
				ab2 = Relationship(service, "服务使用协议", node)
			else:
				print(i[2])
				ser = Node("服务", name=i[2])
				ab3 = Relationship(ser_node, "服务使用协议", ser)
				graph.create(ab3)
				ab2 = Relationship(ser, "服务使用协议", node)
			graph.create(ab2)


finally:
	f.close()