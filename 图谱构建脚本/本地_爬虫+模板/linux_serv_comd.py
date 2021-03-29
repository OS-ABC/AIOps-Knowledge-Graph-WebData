# encoding=utf8
#此脚本式为linux中的命令和服务建立关系（当前neo4j中只命令和服务概念，只有Linux相关知识）
from bs4 import BeautifulSoup
from py2neo import Graph,Node,Relationship

def create_or_fail(start_node_name, end_node_name):
	r="MATCH (n:`服务`)-[r]-(m:`命令`) where n.name='"+start_node_name+"' and m.name='"+end_node_name+"' RETURN type(r)"
	a=graph.run(r)
	if a:
		return True
	else:
		return False
		
#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

f = open("./file/linux_serv_comd_dic.txt")
try:
	content = eval(f.read())
	for ele in content:
		if content[ele]:
			# print(ele)
			serv_node = graph.nodes.match("服务",name=str(ele)).first()
			# print(serv)
			for comd in content[ele]:
				if content[ele][comd] - 6 > 0:
					comd_node = graph.nodes.match("命令",name=str(comd)).first()
					# print(comd)
					a = create_or_fail(str(ele),str(comd))
					print(str(ele)+":::"+str(comd)+":::"+str(a))
					if a:
						ab = Relationship(serv_node, "服务使用命令", comd_node)
						graph.create(ab)
finally:
	f.close()

