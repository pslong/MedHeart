#!/usr/bin/env python3

import torch
from transformers import AutoModelForCausalLM
from loguru import logger

__all__ = ["load_model_tokenizer", "generate", "inference"]


def load_model_tokenizer(
    path: str = None, model_size: str = "7b", model_type: str = "base",
    device_map: str = "auto", **tokenizer_kwargs
):
    assert model_size in ("7b", "13b")
    assert model_type in ("base", "chat")
    if model_size == "7b":
        if model_type == "base":
            from base_7b.tokenization_baichuan import BaichuanTokenizer  # relative import
        elif model_type == "chat":
            from chat_7b.tokenization_baichuan import BaichuanTokenizer  # relative import
    elif model_size == "13b": 
        if model_type == "base":
            from base_13b.tokenization_baichuan import BaichuanTokenizer  # relative import
        elif model_type == "chat":
            from chat_13b.tokenization_baichuan import BaichuanTokenizer  # relative import
    else:
        raise ValueError(f"Model size {model_size} not supported. Plz use 13b/7b")

    if path is None:
        path = f"/home/ubuntu/bc2/{model_type}_{model_size}"
    # config = AutoConfig.from_pretrained(path, local_files_only=True, trust_remote_code=True)
    # print(config)

    tokenizer = BaichuanTokenizer.from_pretrained(
        path, use_fast=True, local_files_only=True, **tokenizer_kwargs
    )
    model = AutoModelForCausalLM.from_pretrained(path, device_map=device_map, trust_remote_code=True)
    return model, tokenizer


def generate(inputs, model, tokenizer, **kwargs) -> str:
    max_new_tokens = kwargs.pop("max_new_tokens", 64)
    repeat_penalty = kwargs.pop("repetition_penalty", 1.1)
    inputs = tokenizer(inputs, return_tensors='pt')
    inputs = inputs.to('cuda:0')
    pred = model.generate(**inputs, max_new_tokens=max_new_tokens, repetition_penalty=repeat_penalty, **kwargs)
    response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)
    return response


@logger.catch(reraise=True)
def inference(model_size: str = "7b", model_type: str = "base"):
    model, tokenizer = load_model_tokenizer(model_size=model_size, model_type=model_type)
    inputs = '登鹳雀楼->王之涣\n夜雨寄北->'
    print(generate(inputs, model, tokenizer))


if __name__ == "__main__":
    inference(model_size="7b", model_type="base")
