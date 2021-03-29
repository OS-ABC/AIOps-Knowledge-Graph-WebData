# encoding=utf8
from py2neo import Graph,Node,Relationship



graph = Graph("http://localhost:7474",auth=("neo4j","12345"))
com_node = graph.nodes.match("命令",name='snap').first()

data =graph.run("match (n:`技术`)-[r:`技术有关的服务`]->(m:`服务`) where n.name='hadoop' and m.name='namanode' return r")
if data:
	print(data)
