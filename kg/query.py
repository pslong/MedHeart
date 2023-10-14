from py2neo import Graph, Node, Relationship
from py2neo.matching import *
import json

class QueryData:
    def __init__(self):
        self.graph = Graph("http://localhost:7474/", auth=("neo4j", "12345678"),name="neo4j")
    
    def QueryNode(node:str):
        # 取节点
        query = f"MATCH (n:{node}) RETURN {json.loads(n)}"
        result = self.graph.run(query)
        for record in result:
            node = record['n']
            # 在这里处理节点对象 node
            print(node)

    def QueryNodeWhere(node:str,property_key:str,property_value:str):
        # 根据条件查找
        property_key = "name"  # 替换为你要查找的属性键
        property_value = "心脏病"  # 替换为你要查找的属性值
        query = f"MATCH (n:疾病) WHERE n.{property_key} = '{property_value}' RETURN n"
        result = self.graph.run(query)
        for record in result:
            node = record['n']
            # 在这里处理节点对象 node
            print(node)
        # 查询节点
        # result1 = nodes.match("疾病").all()
        # result2 = nodes.match("疾病").all()
        #
        # p1 = result1[0]
        # p2 = result2[0]
        # print(result1)
        # # 查询关系
        # matcher = RelationshipMatcher(self.graph)
        # result4 = matcher.match([p1,p2], r_type=None).all()
        # print(result4)
        # for r in result4:
        #     print(r)

        # for record in result:
        #     print(record['name'])




if __name__ == '__main__':
    qd = QueryData()
    qd.QueryNodeWhere("疾病","name","心脏病")