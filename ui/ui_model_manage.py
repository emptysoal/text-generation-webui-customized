# -*- coding: utf-8 -*-

import gradio as gr

from llm.model_manage import get_models_name, load_model


def create_model_manage_ui():
    with gr.Tab("模型管理"):
        with gr.Row():
            name_dropdown = gr.Dropdown(label="选择一个模型", choices=get_models_name(), value="无", scale=3)
            btn = gr.Button("加载", scale=1)
        output = gr.Textbox(show_label=False)

        # 绑定事件，加载模型
        btn.click(load_model, inputs=name_dropdown, outputs=output)
