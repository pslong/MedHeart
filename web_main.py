#!/usr/bin/env python3

import json
import torch
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from loguru import logger
from api.baichuan_api import get_symptoms,do_request
from tencent_vector import searchByText
from kg.query import QueryData
import re
from find_diseases import findPossibleDisease

from modeling import load_model_tokenizer, generate  # reletive import

st.set_page_config(page_title="Baichuan 2")
st.title("Baichuan 2")

init_model = st.cache_resource(load_model_tokenizer)


def clear_chat_history():
    del st.session_state.messages


def init_chat_history():
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是心血管疾病预诊大模型，很高兴为您服务🥰")

    if "messages" in st.session_state:
        for message in st.session_state.messages:
            avatar = '🧑‍💻' if message["role"] == "user" else '🤖'
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    else:
        st.session_state.messages = []

    return st.session_state.messages


@logger.catch(reraise=True)
def main():
    model, tokenizer = init_model(model_size="13b")    
    qd = QueryData()
    messages = init_chat_history()

    if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(prompt)
        messages.append({"role": "user", "content": prompt})
        print(f"[user] {prompt}", flush=True)
        with st.chat_message("assistant", avatar='👩🏻‍⚕️'):
            placeholder = st.empty()

            # 从prompt中提取需要检索的症状
            ymptoms = get_symptoms(prompt) # 
            if ymptoms!='无':
                symptoms_list = re.split(r",|，| |、", ymptoms)
                v_symptoms_sim = []
                symptoms_kg_dic = {}
                if len(messages)<=1:
                    for ymptom in symptoms_list:
                        # 从向量库中，检索出相似的标准症状词
                        v_ymptoms = searchByText(ymptom)
                        v_symptoms_sim = list(set(v_symptoms_sim + v_ymptoms))
                    response = "根据反馈的症状，您需进一步准确选择，以下您可能有的症状：" + '、'.join(v_symptoms_sim)
                    prompt_desc = "请对以下症状进行简洁的说明：" + '、'.join(v_symptoms_sim)
                    res_sim = do_request(prompt_desc)

                    response = response + '。\n' + res_sim 
                else:
                # 从知识图谱中检索出症状对应的，可反问用户的症状 以及 要区分的疾病。QuerySymptomAndDiseases
                    for symptom in symptoms_list:
                        kg_res = qd.QuerySymptomAndDisease(symptom)
                        for disease in kg_res:
                            symptoms_kg_dic[disease] = kg_res[disease]
                    #symptoms_kg_dic = qd.QuerySymptomAndDiseases(symptoms_list);
                    diseases_to_decide,symptoms_for_ask = findPossibleDisease(symptoms_kg_dic, symptoms_list)
                    if len(symptoms_for_ask)==0 or len(diseases_to_decide) <= 3:
                        response ="疑似疾病个数 " + str(len(diseases_to_decide))  + '  疾病名称：'+ '、'.join(diseases_to_decide)
                        prompt_out = "请从病因，症状，检查项，治疗方式四方面对以下疾病：" + '、'.join(diseases_to_decide) + "进行详细的介绍"
                        res_out = do_request(prompt_out)
                        response = response  + '\n' + res_out ; 
                    else:
                        response = "根据反馈的症状，对疾病 【 " + '、'.join(diseases_to_decide) +"】进一步排查 ， \n   请告知您是否有症状：" + '、'.join(symptoms_for_ask)

            else: 
                model = AutoModelForCausalLM.from_pretrained("output1", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
                response = generate(prompt, model, tokenizer)
                print(response)
            placeholder.markdown(response)
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
        messages.append({"role": "assistant", "content": response})
        print(json.dumps(messages, ensure_ascii=False), flush=True)

        st.button("清空对话", on_click=clear_chat_history)


if __name__ == "__main__":
    main()
