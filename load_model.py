from modeling import load_model_tokenizer, generate  # reletive import
import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


st.set_page_config(page_title="Baichuan 2")
st.title("Baichuan 2")

init_model = st.cache_resource(load_model_tokenizer)
tokenizer = init_model(model_size="13b")
model = AutoModelForCausalLM.from_pretrained("output", device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)