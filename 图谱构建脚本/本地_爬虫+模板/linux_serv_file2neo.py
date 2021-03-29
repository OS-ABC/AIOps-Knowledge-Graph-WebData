# encoding=utf8
#此脚本式为linux中的配置文件和服务建立关系（当前neo4j中只命令和服务概念，只有Linux相关知识）
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship

def create_or_fail(start_node_name, file):
	r="MATCH (n:`服务`)-[r]-(m:`配置文件`) where n.name='"+start_node_name+"' and m.path=~'.*"+file+".*' RETURN type(r)"
	if r:
		return True
	else:
		return False
		
#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))
root = graph.nodes.match("配置文件",name='配置文件').first()
f = open("./file/linux_serv_file_dic.txt")
try:
	content = eval(f.read())
	for ele in content:
		if content[ele]:
			# print(ele)
			serv_node = graph.nodes.match("服务",name=str(ele)).first()
			# print(serv)
			for file in content[ele]:
				if content[ele][file]>=3:
					file_cypher="match (m:`配置文件`) where m.path=~'.*"+file+".*' return m"
					a = graph.run(file_cypher)
					if list(a):
						ab = Relationship(serv_node, "服务使用配置文件", a[0])
						graph.create(ab)
					else:
						file_node=Node("配置文件", name=file,path=file)
						bb = Relationship(root, "包含", file_node)
						abc = Relationship(serv_node, "服务使用配置文件", file_node)
						graph.create(abc)
						graph.create(bb)
finally:
	f.close()

