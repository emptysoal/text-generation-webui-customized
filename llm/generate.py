# -*- coding: utf-8 -*-

from threading import Thread

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import TextIteratorStreamer


class Generator:
    def __init__(self, model_name="../Qwen2-1.5B-Instruct"):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        # self.messages = [
        #     {"role": "system", "content": "You are a helpful assistant."}
        # ]

    def build_input(self, chat_history):
        """
            接收聊天记录，然后转换为 LLM 所识别的格式
        :param chat_history: 聊天记录 - [["user message", "bot message"], [...], ...]
        :return: LLM 的输入格式
        """

        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

        for user_messaege, bot_message in chat_history:
            if user_messaege:
                messages.append({"role": "user", "content": user_messaege})
            if bot_message:
                messages.append({"role": "assistant", "content": bot_message})

        # 再把上述聊天内容转为 token
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True, )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        return model_inputs

    def text_generate(self):
        chat_history = []

        while True:
            prompt = input("Question: ")
            if prompt == "quit":
                break

            chat_history.append([prompt, None])
            model_inputs = self.build_input(chat_history)

            generation_kwargs = dict(model_inputs, streamer=self.streamer, max_new_tokens=1024)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()

            generated_text = ""
            for new_text in self.streamer:
                print(new_text, end="")
                generated_text += new_text
            print()

            chat_history[-1][1] = generated_text

            thread.join()


if __name__ == '__main__':
    gen = Generator("../../Qwen2-1.5B-Instruct")
    gen.text_generate()
