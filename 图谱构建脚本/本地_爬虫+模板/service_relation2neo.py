# encoding=utf8
from py2neo import Graph,Node,Relationship

#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","SSPKUsspku12345"))

f=open("./file/service_comd_file.txt","r",encoding='utf8')
command_root = graph.nodes.match("命令",name="命令").first()
serv_root = graph.nodes.match("服务",name="服务").first()
file_root = graph.nodes.match("配置文件",name="配置文件").first()
tech_root = graph.nodes.match("技术",name="技术").first()
com_temp = 0
serv_temp = 0
file_temp = 0

try:
	content = f.read()
	relation_list = content.split('\n')
	# print(len(relation_list))
	i = 0
	for evey_list in relation_list:
		# print(i%4)
		if (i%3) == 0:
			com_list = evey_list.split(":::")
			name = com_list[0]
			com_dic = eval(com_list[1])
			tech_node = graph.nodes.match("服务",name=name).first()
			if not tech_node:
				tech_node = Node("服务", name=name,platform='linux')
				aa = Relationship(tech_root, "包含服务", tech_node)
				graph.create(aa)

			for k,v in com_dic.items():
				if v > com_temp:
					com_node = graph.nodes.match("命令",name=k,platform='linux').first()
					print(name)
					# print(com_node)
					if com_node:
						data =graph.run("match (n:`服务`)-[r:`服务使用命令`]->(m:`命令`) where n.name='"+name+"' and m.name='"+k+"' return r")
						if not data:
							ab = Relationship(tech_node, "服务使用命令", com_node)
							graph.create(ab)
					else:
						com_node = Node("命令", name=k,platform='linux')
						ab1 = Relationship(command_root, "包含命令", com_node)
						graph.create(ab1)
						ab2 = Relationship(tech_node, "服务使用命令", com_node)
						graph.create(ab2)


		elif (i%3) == 1:
			file_list = evey_list.split(":::")
			name = file_list[0]
			# print(file_list[0])
			file_dic = eval(file_list[1])
			tech_node = graph.nodes.match("服务",name=name).first()
			if not tech_node:
				tech_node = Node("服务", name=name,platform='linux')
				aa = Relationship(tech_root, "包含服务", tech_node)
				graph.create(aa)
			for k,v in file_dic.items():
				if v > file_temp and "//" not in k and " " not in k and "www" not in k and k is not '/' and k is not '/.':
					file_node = graph.nodes.match("配置文件",name=k).first()
					print(name)
					if file_node:
						data =graph.run("match (n:`服务`)-[r:`服务使用配置文件`]->(m:`配置文件`) where n.name='"+name+"' and m.name='"+k+"' return r")
						if not data:
							ad = Relationship(tech_node, "服务使用配置文件", file_node)
							graph.create(ad)
					else:
						file_node = Node("配置文件", name=k, path=k,platform='linux')
						ad1 = Relationship(file_root, "包含配置文件", file_node)
						graph.create(ad1)
						ad2 = Relationship(tech_node, "服务使用配置文件", file_node)
						graph.create(ad2)
		else:
			i = i + 1
			continue
		i = i + 1

finally:
	f.close()