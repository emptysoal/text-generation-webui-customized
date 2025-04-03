# -*- coding: utf-8 -*-

from threading import Thread
import gradio as gr

from llm.model_manage import in_use_model_instance
from tools.make_logger import Logger

logger = Logger().get_logger(__name__)


def user(user_message, history):
    if user_message != "":  # 用户输入为空时，就不新增对话了
        history.append([user_message, None])

    return "", history


# 定义聊天机器人逻辑
def bot(history):
    if history[-1][1] is None:  # 用户消息有效
        # 获取大语言模型实例
        generator = in_use_model_instance.get("model_instance", None)
        if not generator:
            raise gr.Error("没有预加载好的模型，请前往模型管理页加载模型。")

        # 1. 聊天记录转为 LLM 需要的输入格式
        model_inputs = generator.build_input(history)
        # 2. 开启线程异步推理
        generation_kwargs = dict(model_inputs, streamer=generator.streamer, max_new_tokens=2048)
        thread = Thread(target=generator.model.generate, kwargs=generation_kwargs)
        thread.start()
        # 3. 输出 LLM 文本生成结果
        history[-1][1] = ""
        for new_text in generator.streamer:
            history[-1][1] += new_text
            yield history
        thread.join()
    else:  # 用户消息无效，空字符串或者其它
        yield history


def clear_fun():
    # 初始化用户输入框，历史聊天记录
    return "", [[None, "很高兴能够与你进行交流"]]


def create_chat_ui():
    with gr.Tab("问答聊天"):
        with gr.Column():
            # 创建 Chatbot 组件
            first_chat_message = [[None, "很高兴能够与你进行交流"]]
            chatbot = gr.Chatbot(
                value=first_chat_message,
                label="聊天记录",
                height=400,
                show_label=False,
                avatar_images=("./icons/user.jpeg", "./icons/assistant.jpeg")
            )

            with gr.Row():
                # 创建输入框
                msg = gr.Textbox(label="输入消息", placeholder="请输入消息...", scale=6, show_label=False)
                # 创建状态组件，用于保存聊天历史
                # 创建提交按钮
                submit = gr.Button("发送", scale=1)
                clear = gr.Button("清除", scale=1)

        # 绑定事件
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
        submit.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
        clear.click(clear_fun, outputs=[msg, chatbot])
