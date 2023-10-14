#!/usr/bin/env python3

import json
import torch
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
from loguru import logger

from modeling import load_model_tokenizer, generate  # reletive import

st.set_page_config(page_title="Baichuan 2")
st.title("Baichuan 2")

init_model = st.cache_resource(load_model_tokenizer)


def clear_chat_history():
    del st.session_state.messages


def init_chat_history():
    with st.chat_message("assistant", avatar='🤖'):
        st.markdown("您好，我是百川大模型，很高兴为您服务🥰")

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
    model = AutoModelForCausalLM.from_pretrained("output1", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
    messages = init_chat_history()

    if prompt := st.chat_input("Shift + Enter 换行, Enter 发送"):
        with st.chat_message("user", avatar='🧑‍💻'):
            st.markdown(prompt)
        messages.append({"role": "user", "content": prompt})
        print(f"[user] {prompt}", flush=True)
        with st.chat_message("assistant", avatar='👩🏻‍⚕️'):
            placeholder = st.empty()
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
