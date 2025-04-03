# -*- coding: utf-8 -*-

import gradio as gr

from ui.ui_chat import create_chat_ui
from ui.ui_model_manage import create_model_manage_ui


def create_interface():
    # 创建 Gradio 界面
    with gr.Blocks() as app:
        with gr.Column():
            gr.Markdown(" # <center>自制 LLM Interface 问答交流助手</center>")
            gr.Markdown(" ###### <center>Made by dong hong da</center>")

            create_chat_ui()
            create_model_manage_ui()

    app.queue()
    app.launch(server_name="0.0.0.0")


if __name__ == '__main__':
    create_interface()
