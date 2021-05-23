# 图谱构建
***
本文图谱通过编写python脚本的方式抽取知识，在本文件加下是python脚本，在file文件夹下的是知识整理。
有很多python脚本文件，大部分是没啥实际作用的，有的是我做实验的脚本，最后没有用在项目里，有的是处理数据存入neo4j的脚本。
脚本
以下是部分处理脚本，有些没有在我这一版图谱中用上，但是不代表它们未来不会用上，目前这一版知识图谱是为了完成知识介绍任务构造的
***
（废弃）Scrapy_test文件夹及里面的文件
这个文件夹下的程序都没有实际作用，是我做爬虫实验用的

（废弃）agreement.py是把协议实体写入数据库的脚本
协议实体在后期被去掉了

Change_node_param.py与Change_node_param2.py是统一知识图谱中命令参数格式

comd_detail2neo.py有些命令没有介绍，把用模板抽取的介绍录入neo4j

（实验）entity_data.py把实体的属性信息录入mysql
这个实验需要通过统计定义实体属性，统计python代码在另一个脚本，最终没有利用

（实验）entity_solid.py根据实体属性计算实体对齐，成对匹配
这个计算过程是基于entity_data.py把实体属性录入mysql后做的，没有被利用

（测试）file_count.py计算爬虫中文件的数量，没啥用，当初需要有文件总数

get_neo4j_nodes.py获取neo4j中没有介绍的命令实体名称，并打印出来
这个脚本是想得到没有介绍属性或是介绍属性的value为空的命令实体，修改某个字段可以变成获取服务的实体，或是获取文件的实体，这一脚本就够用了

hadoop_linux_command.py这个脚本是录入hadoop，hdfs，yarn，mapreduce相关命令
当时有一个外网的服务器，从那个服务器上读取数据，录入到本地的服务器上

hadoop_linux_component.py这个脚本是录入组件信息的，和上一个脚本一样

hadoop_linux_file.py这个脚本是录入配置文件信息的，和上一个脚本一样

（测试）jiebatest.py用来写分词测试的脚本，基本上跟jieba分词的测试都先在这个脚本上本地测试一下

KG_introduce.py根据规则模板爬取实体介绍
这个脚本会把爬取的数据用log的方式存入serv_detail.log，人工处理一下格式，在通过comd_detail2neo.py录入neo4j

（实验，废弃）language2neo.py爬取语言&框架实体的百科消息盒子信息，主要是做属性存入neo4j中

（改）linux_serv_comd.py为linux中的命令和服务建立关系，爬取的内容在linux_serv_comd_dic.txt，在另一个脚本中，优化了抽取规则方法

（改）linux_serv_file.py这个脚本用来爬取服务与配置文件的关系，并对关系个数做统计，结果存入serv_file_dic.txt，在另一个脚本中，优化了抽取规则方法

linux_serv_file2neo.py为linux中的配置文件和服务建立关系，存入neo4j

（改）linux_service_commad.py抽取服务与命令的关系，在另一个脚本中会对抽取规则做改动

min_edit.py最小编辑距离

（废弃）new_entity_ex.py实体抽取，没啥用

（实验）qulity_ex.py根据统计学原理，分析实体属性。最后没用上，是一个方向吧
获取某一类实体的百科页面，统计百科页面中出现次数最多的名词，过滤这些名词，选择可以成为属性的名词。

serv_commd_predict.py设定阈值，确定测试集中准确率最高是阈值是多少。
这个是用来预测关系抽取中阈值设置的，只需修改测试集和参数，就可以确定不同阈值

serv_detail2neo.py服务的详情录入neo4j。
有些服务实体没有详情，把服务详情录入neo4j，应该会有另一个脚本爬取详情的信息。

service.py服务实体信息录入neo4j。

service_comd_file.py这个是最终版本，抽取服务和命令、配置文件的关系，由于是根据技术抽取脚本改的，里面很多变量名称还是看着不太对劲。

service_relation2neo.py服务与命令，服务于配置文件，录入neo4j

（改）service_spider.py服务关系爬取脚本，比较早的版本

（废弃）snap_test.py没啥用，忘了这个是干啥的了

Solid_alignment.py局部集体对齐算法，这个脚本改一些变量就可以对齐其他的实体，只考虑实体名称

（实验）tech_atr.py这个脚本是根据统计获取的实体属性，抽取属性值，最后没用上，感觉是一个方向吧，反正我这一版没有用上

tech_comd_dic.py技术实体关系抽取。最终版

tech_relation2neo4j.py技术实体关系录入neo4j

（实验）tech_similar_count.py忘了这个要干啥了，好像是处理实体属性的

tech2neo.py把技术实体录入neo4j，录入过程中爬取了百科消息盒子作为属性

（实验）translate2.py翻译插件实验

（废弃）windows_serv2neo4j.py想录入windows的服务，最后没用上

（实验）words_similar.py句子相似度实验，TF-IDF
