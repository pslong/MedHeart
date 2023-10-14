from py2neo import Graph
import os
from tqdm import tqdm
import json


class CreateKG:
    # 写一个 Graph 连接neo4j数据库的方法，neo4j数据库的地址是本地的，端口号是7687，用户名是neo4j，密码是12345678

    def __init__(self, kg_host, kg_port, kg_user, kg_password, data_path):
        self.graph = Graph("http://localhost:7474/", auth=(kg_user, kg_password),name="neo4j")
        print(self.graph)

        if not data_path or data_path == '':
            raise Exception("数据集地址为空")
        if not os.path.exists(data_path):
            raise Exception("数据集不存在")
        self.data_path = data_path

    def saveEntity(self, label, data):
        print("\n写入实体：", label)
        for item in tqdm(data, ncols=80):
            try:
                property = {}
                for key, value in item.items():
                    if isinstance(value, str):
                      value = value.replace("'", "")
                      property[key] = value
                      # property.append(key + ":" + "'" + value + "'")
                    else:
                      property[key] = json.dumps(value)
                      # property.append(key + ":" + str(value))
                if len(property) == 0:
                    continue

                print(property)
                property_str = json.dumps(property)
                cql = f"MERGE (n:{label} {{ properties: $properties }})"
                self.graph.run(cql, parameters={"properties": property_str})
                # cql = f"MERGE (n:{label} {{ {property_string} }})"
                # print(cql)
                # cql = "MERGE(n:" + label + "{" + ",".join(property) + "})"
                # self.graph.run(cql)
            except Exception as e:
                print("Error:", e)

    def saveRelation(self, s_label, e_label, label, data):
        print("\n写入关系：", label)
        for item in tqdm(data, ncols=80):
            try:
                s_name = item["s_name"]
                e_name = item["e_name"]
                cql = "MATCH(p:" + s_label + "),(q:" + e_label + ") WHERE p.name='" + s_name + "' AND q.name='" + e_name + "' MERGE (p)-[r:" + label + "]->(q)"
                print(cql)
                self.graph.run(cql)
            except Exception as e:
                print("Error:", e)

    def getValue(self, key, data):
        if key in data:
            return data[key]
        return ""

    def init(self):
        # 实体
        # 疾病
        diseases = []
        # 疾病症状
        symptoms = []
        # 检查项目
        checks = []


        # 关系
        # 疾病症状
        diseaseSymptomRelations = []
        # 疾病检查
        diseaseCheckRelations = []


        with open(self.data_path, 'r') as file:
            # 2. 使用 json.load() 解析 JSON 文件并转换为 Python 字典
            dic = json.load(file)
            for data in dic:
                 disease = {
                    "name": data["name"],
                    "symptom": self.getValue("symptom", data),
                    "cure_department":self.getValue("cure_department",data)
                }
                 diseases.append(disease)
                 # 症状
                 if "symptom" in data:
                     for symptom in data["symptom"]:
                         # 疾病科室关系
                         diseaseSymptomRelations.append({
                             "s_name": data["name"],
                             "e_name": symptom
                         })
                         # 症状实体
                         property = {
                             "name": symptom
                         }
                         if property not in symptoms:
                             symptoms.append(property)

                 # 检查项目
                 if "cure_department" in data:
                     for check in data["cure_department"]:
                         # 疾病科室关系
                         diseaseCheckRelations.append({
                             "s_name": data["name"],
                             "e_name": check
                         })
                         # 检查项目实体
                         property = {
                             "name": check
                         }
                         if property not in checks:
                             checks.append(property)


            # 疾病
        self.saveEntity("疾病", diseases)
        # 疾病症状
        self.saveEntity("疾病症状", symptoms)
        # 检查项目
        self.saveEntity("疾病检查项目", checks)


        # 关系
        # 疾病症状
        self.saveRelation("disease", "symptom", "疾病症状关系", diseaseSymptomRelations)
        # 疾病检查
        self.saveRelation("disease", "check", "疾病检查关系", diseaseCheckRelations)



if __name__ == '__main__':
    kg_host = "127.0.0.1"
    kg_port = 7687
    kg_user = "neo4j"
    kg_password = "12345678"
    data_path = "/home/ubuntu/bc2/kg/disease_simple_doctor_check.json"
    kg = CreateKG(kg_host, kg_port, kg_user, kg_password, data_path)
    kg.init()
