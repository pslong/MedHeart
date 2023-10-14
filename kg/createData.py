import openai2 as openai
import json

# 替换为你的 OpenAI API 密钥
api_key = "YOUR_API_KEY"

# 输入疾病名称列表
diseases = ['动脉粥样硬化', '肺动脉高压', '心脏神经官能症', ...]  # 疾病名称列表

# 创建一个空的 JSON 数据模板
data_template = {
    "_id": {"$oid": ""},
    "name": "",
    "desc": "",
    "category": [],
    "prevent": "",
    "cause": "",
    "symptom": [],
    "get_prob": "",
    "get_way": "",
    "acompany": [],
    "cure_department": [],
    "cure_way": [],
    "cure_lasttime": "",
    "cured_prob": "",
    "cost_money": "",
    "check": [],
    "recommand_drug": [],
    "drug_detail": []
}

# 初始化 OpenAI API 客户端
openai.api_key = api_key

# 用 GPT-3 生成填充数据
filled_data = []
for disease_name in diseases:
    # 设置模型提示
    prompt = f"生成关于{disease_name}的疾病信息："
    # 调用 GPT-3 生成数据
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150  # 根据需要适当调整生成文本的长度
    )
    # 解析生成的文本并填充到数据模板
    generated_text = response.choices[0].text.strip()
    data = data_template.copy()
    data["name"] = disease_name
    data["desc"] = generated_text
    filled_data.append(data)

# 将填充后的数据保存为 JSON 文件
with open("disease_data.json", "w") as json_file:
    json.dump(filled_data, json_file, indent=4)
