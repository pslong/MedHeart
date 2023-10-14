from py2neo import Graph, Node, Relationship
from py2neo.matching import *
import json
import ast

class QueryData:
    def __init__(self):
        self.graph = Graph("http://localhost:7474/", auth=("neo4j", "12345678"),name="neo4j")
    
    def QueryNode(self,node:str):
        # 取节点
        query = f"MATCH (n:{node})  RETURN n "
        result = self.graph.run(query)
        result_array = []
        for record in result:
            node = record['n']
            result_array.append(node.get('name'))
        return result_array

    # 通过疾病查找症状
    def QuerySymptomWithDisease(self,disease:str):
        query = f"MATCH (n:疾病)-[e:疾病症状关系]->(n1:疾病症状) where n.name = '{disease}' return n,n1"
        result = self.graph.run(query)
        array = []
        for item in result:
            node = item['n1']
            array.append(node.get('name'))
        return array
    
    # 通过症状查找疾病
    def QueryDiseaseWithSymptom(self,symptom:str):
        query = f"MATCH (n:疾病症状)-[e:症状疾病关系]->(n1:疾病) where n.name = '{symptom}' return n,n1"
        result = self.graph.run(query)
        array = []
        for item in result:
            node = item['n1']
            array.append(node.get('name'))
        return array
    
    # 通过疾病查找检查项
    def QueryCheckWithDisease(self,disease:str):
        query = f"MATCH (n:疾病)-[e:疾病检查关系]->(n1:疾病检查项目) where n.name = '{disease}' return n,n1"
        result = self.graph.run(query)
        array = []
        for item in result:
            node = item['n1']
            array.append(node.get('name'))
        return array
    # 通过症状查找疾病，再通过疾病查找症状
    def QuerySymptomAndDisease(self,symptom:str):
        result = {}
        disease = self.QueryDiseaseWithSymptom(symptom)
        disease_dict = {}
        for item in disease:
            symptoms = self.QuerySymptomWithDisease(item)
            disease_dict[item] = symptoms
        result[symptom] = disease_dict
        return disease_dict
    # 同时多个症状对应的疾病
    def QuerySymptomAndDiseases(self,symptomList:[str]):
        result = {}
        common_elements = []
        for symptom_item in symptomList:
            for symptom_item2 in symptomList:
                if symptom_item == symptom_item2:
                    continue
                else:
                    disease1 = self.QueryDiseaseWithSymptom(symptom_item)
                    disease2 = self.QueryDiseaseWithSymptom(symptom_item2)
                    common_elements = list(set(disease1) & set(disease2))
                    continue
        disease_dict = {}
        for item in common_elements:
            symptoms = self.QuerySymptomWithDisease(item)
            disease_dict[item] = symptoms
        result_string = " ".join(symptomList)
        result[result_string] = disease_dict
        return result,disease_dict
    
if __name__ == '__main__':
    qd = QueryData()
    # 根据实体查找对应的所有项
    node = qd.QueryNode('疾病')
    # print(f"所有疾病:{node}")

    # 根据疾病查找所要检查的项目
    check_result = qd.QueryCheckWithDisease("房性心动过速")
    # print(f"疾病检查项目：{check_result}")

    # 根据疾病查找对应的全部症状
    symptom_result = qd.QuerySymptomWithDisease("房性心动过速")
    # print(f"疾病的症状：{symptom_result}")

    # 根据症状查找疾病
    disease_result = qd.QueryDiseaseWithSymptom("心慌")
    #print(f"症状对应疾病:{disease_result}")

    # 通过症状查找疾病，再通过疾病查找症状
    disease_dict = qd.QuerySymptomAndDisease("心悸")
    print(f"症状对应疾病，疾病对应症状:{disease_dict}")

    # 搜索多个症状对应的疾病 比如都有心悸胸闷症状的疾病
    more_result = qd.QuerySymptomAndDiseases(['头晕','乏力'])
    #print(more_result)

