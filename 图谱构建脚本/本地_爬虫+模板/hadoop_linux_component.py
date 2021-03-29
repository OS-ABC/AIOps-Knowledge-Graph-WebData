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

data = graph2.run("MATCH (m:component)-[r]->(n:component) where m.name='component' RETURN n").data()

hadoop_node = graph.nodes.match("技术",name="hadoop").first()
for ele in data:
	new_data = build_nodes(ele)
	component_node = graph.nodes.match("技术",name=new_data['name']).first()
	if component_node:
		component_node['platform']='hadoop'
		component_node['detail'] = new_data['detail']
		ab2 = Relationship(hadoop_node, "相关组件", component_node)
		graph.create(ab2)
	else:
		com_node = Node("技术", name=new_data['name'],detail=new_data['detail'],platform='hadoop')
		ab2 = Relationship(hadoop_node, "相关组件", com_node)
		graph.create(ab2)

data = graph2.run("MATCH (m:tools)-[r]->(n:tools) where m.name='tools' RETURN n").data()
for ele in data:
	new_data = build_nodes(ele)
	component_node = graph.nodes.match("技术",name=new_data['name']).first()
	if component_node:
		component_node['platform']='hadoop'
		component_node['detail'] = new_data['detail']
		ab2 = Relationship(hadoop_node, "相关组件", component_node)
		graph.create(ab2)
	else:
		com_node = Node("技术", name=new_data['name'],detail=new_data['detail'],platform='hadoop')
		ab2 = Relationship(hadoop_node, "相关组件", com_node)
		graph.create(ab2)