import requests
import json
import time
import hashlib
import ast



def calculate_md5(input_string):
    md5 = hashlib.md5()
    md5.update(input_string.encode('utf-8'))
    encrypted = md5.hexdigest()
    return encrypted

def do_request(content):
    url = "https://api.baichuan-ai.com/v1/chat"
    api_key = "f412c9822c62e4fe037916c1365bf603"
    secret_key = "okEEqzb3g04z6HyfREQW6eS6imY="

    data = {
        "model": "Baichuan2-53B",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }

    json_data = json.dumps(data)
    time_stamp = int(time.time())
    signature = calculate_md5(secret_key + json_data + str(time_stamp))

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key,
        "X-BC-Request-Id": "your requestId",
        "X-BC-Timestamp": str(time_stamp),
        "X-BC-Signature": signature,
        "X-BC-Sign-Algo": "MD5",
    }

    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        print("请求成功！")
        print("响应header:", response.headers)
        print("响应body:", response.text)
        rtext = json.loads(response.text)
        res = rtext['data']['messages'][0]['content']
        return res
    else:
        return "请求失败，状态码:"+ str(response.status_code)

def prompt_get(query):
    # prompt=''' 
    #     你是心血管疾病专家
    #     你需要根据用户的输入【query】，从中抽离出用户描述的心血管疾病相关的症状，写入【症状列表】,如果没有描述症状【症状列表】无,不进行其他返回，如：

    #     【query】我最近出现呼吸困难、出汗、恶心、呕吐，心率不齐不知道是什么原因
    #     【症状列表】出汗,恶心,呕吐,心率不齐

    #     根据【query】''' + query + '''【症状列表】 

    # '''

    prompt=''' 
        你是心血管疾病专家
        你需要根据用户的输入，从中抽离出用户描述的心血管疾病相关的症状，如果没有心血管疾病症状，返回原来的用户输入

        如：我最近出现呼吸困难、出汗、恶心、呕吐，心率不齐不知道是什么原因
        只可返回:呼吸困难,出汗,恶心,呕吐,心率不齐

        如：我身体不舒服
        只可返回:无


        用户输入：''' + query + "只可返回"

    
    return prompt

def get_symptoms(query):
    prompt = prompt_get(query)
    return do_request(prompt)


if __name__ == "__main__":
    get_symptoms('我最近总是心跳慢，心慌，请问有什么可能疾病')


              