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

data = graph2.run("MATCH (m:command)-[r]->(n:command) where m.name='command' RETURN n").data()
hadoop_node = graph.nodes.match("技术",name="hadoop").first()
com_root = graph.nodes.match("命令",name="命令").first()
for ele in data:
	new_data = build_nodes(ele)
	com_node = Node("命令", name=new_data['name'],detail=new_data['detail'],platform='hadoop',parameter=new_data['parameter'])
	ab = Relationship(com_root, "包含命令", com_node)
	ab2 = Relationship(hadoop_node, "技术有关的命令", com_node)
	graph.create(ab)
	graph.create(ab2)

data2 = graph2.run("MATCH (m:component)-[r]->(n:command) where m.name='hdfs' RETURN n").data()
hdfs_node = graph.nodes.match("技术",name="hdfs").first()
for ele in data2:
	new_data2 = build_nodes(ele)
	name=new_data2['name']
	node = graph.nodes.match("命令",name=name,platform='hadoop').first()
	ab2 = Relationship(hdfs_node, "技术有关的命令", node)
	graph.create(ab2)

data3 = graph2.run("MATCH (m:component)-[r]->(n:command) where m.name='yarn' RETURN n").data()
yarn_node = graph.nodes.match("技术",name="yarn").first()
for ele in data3:
	new_data3 = build_nodes(ele)
	name=new_data3['name']
	node = graph.nodes.match("命令",name=name,platform='hadoop').first()
	ab2 = Relationship(yarn_node, "技术有关的命令", node)
	graph.create(ab2)

data3 = graph2.run("MATCH (m:component)-[r]->(n:command) where m.name='mapreduce' RETURN n").data()
mapreduce_node = graph.nodes.match("技术",name="mapreduce").first()
for ele in data3:
	new_data3 = build_nodes(ele)
	name=new_data3['name']
	node = graph.nodes.match("命令",name=name,platform='hadoop').first()
	ab2 = Relationship(mapreduce_node, "技术有关的命令", node)
	graph.create(ab2)