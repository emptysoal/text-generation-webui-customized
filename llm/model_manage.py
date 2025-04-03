# -*- coding: utf-8 -*-

import os

from llm.generate import Generator
from tools.make_logger import Logger

logger = Logger().get_logger(__name__)

in_use_model_instance = {}


def get_models_name():
    models_dir = "./models"
    model_name_list = ["无"]
    for model_name in os.listdir(models_dir):
        model_path = os.path.join(models_dir, model_name)
        if os.path.isdir(model_path):
            model_name_list.append(model_name)

    return model_name_list


def load_model(model_name):
    # 释放之前加载的模型
    if "model_instance" in in_use_model_instance:
        del in_use_model_instance["model_instance"]

    # 加载新模型
    if model_name != "无":
        model_path = os.path.join("./models", model_name)
        in_use_model_instance["model_instance"] = Generator(model_name=model_path)

    msg = f"Model: '{model_name}' loaded!"
    logger.info(msg)

    return msg
