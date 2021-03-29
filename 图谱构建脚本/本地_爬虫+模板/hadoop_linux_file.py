# encoding=utf8
from py2neo import Graph,Node,Relationship

def build_nodes(nodes_record):
	data = {"id": str(nodes_record.get('n').identity),
			"label": next(iter(nodes_record.get('n').labels))}
	data.update(nodes_record.get('n'))
	return data

#登录neo4j
graph = Graph("http://localhost:7474",auth=("neo4j","12345"))

graph2 = Graph("http://121.36.99.228:7474",auth=("neo4j","SSPKUsspku12345"))

data = graph2.run("MATCH (m:configuration_file)-[r]->(n:configuration_file) where m.name='configuration_file' RETURN n").data()

hadoop_node = graph.nodes.match("技术",name="hadoop").first()
yarn_node = graph.nodes.match("技术",name="yarn").first()

for ele in data:
	new_data = build_nodes(ele)
	# print(new_data['name'])
	com_node = Node("配置文件", name=new_data['name'],detail=new_data['detail'],platform='hadoop',path=new_data['path'])
	ab2 = Relationship(hadoop_node, "技术有关配置文件", com_node)
	graph.create(ab2)

data2 = graph2.run("MATCH (m:component)-[r]->(n:configuration_file) where m.name='yarn' RETURN n").data()

for ele in data2:
	new_data2 = build_nodes(ele)
	com_node2 = Node("配置文件", name=new_data2['name'],detail=new_data2['detail'],platform='hadoop',path=new_data2['path'])
	ab2 = Relationship(yarn_node, "技术有关配置文件", com_node2)
	graph.create(ab2)