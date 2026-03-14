import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI


def create_a_request(user_prompt:{str:str} = {}, assistant_prompt:{str:str} = {}, system_prompt:{str:str} = {}, image_path:{str:str} = {}):
    """
    不建议创建空的请求
    这里是创建请求整理的约定四段格式

    user_prompt = {"role":"user","1":"a","2":"b","3":"c"}
    assistant_prompt = {"role":"assistant","1":"a1","2":"b1","3":"c1"}
    system_prompt = {"role":"system","1":"a2","2":"b2","3":"c2"}
    image_path = {"1":"image.png","2":"image.png","3":"image.png"}
    """

    final_request = []
    # 先添加文本prompts
    list1 = []
    if user_prompt:
        list1.append(user_prompt)
    if assistant_prompt:
        list1.append(assistant_prompt)
    if system_prompt:
        list1.append(system_prompt)
    request_basic = {"role": None, "content": None}
    content = []
    # 这里批量做content
    for item in list1:
        request_basic["role"] = item["role"]
        for key, value in item.items():
            # 这里跳过role
            if key == "role":
                continue
            content.append({"type": "text", "text": key + ":" + value})
        request_basic["content"] = content
        final_request.append(request_basic.copy())
        content = []
        request_basic = {"role": None, "content": None}
    # 再添加图片prompt
    for key, value in image_path.items():
        # 读取图片并转换为base64编码
        with open(value, "rb") as image_file:
            img = Image.open(image_file)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        # 这里做了一条content
        request_basic["role"] = "system"
        content.append({"type": "image_url", "image_url": {"url":f"data:image/png;base64,{image_base64}"}, "file_name": key})
        request_basic["content"] = content
        final_request.append(request_basic.copy())
        content = []
        request_basic = {"role": None, "content": None}

    return final_request

def turn_response_to_text(response):
    # 将响应转换为文本
    text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            text += chunk.choices[0].delta.content
    print("\n文本转化程序的结果：")
    print(text)
    return text

def send_request_get_response(request, model_name, api_url, api_key, max_tokens=1024, temperature=0.8, top_p=0.9):
    """发送请求并获取响应 将响应转换为文本"""
    client = OpenAI(base_url=api_url, api_key=api_key)
    response = client.chat.completions.create(model=model_name, messages=request, stream=True, max_tokens=max_tokens, temperature=temperature, top_p=top_p)
    text = turn_response_to_text(response)
    return text


import datetime

def read_file(file_path):
    """从文件中读取内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    return prompt

def write_to_file(prompt, file_path):
    """将内容写入文件"""
    try:
        bak_path = file_path + ".bak"
        old = ""
        with open(file_path, 'r', encoding='utf-8') as file:
            old = file.read()
        with open(bak_path, 'a', encoding='utf-8') as file:
            file.write("\n" + f"next_prompt:{datetime.datetime.now()}\n" + old)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(prompt)
    except FileNotFoundError as e:
        print(f"文件操作错误: {e}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

# 这里是测试代码
if __name__ == "__main__":
    user_prompt = {"role":"user","1":"a","2":"b","3":"c"}
    assistant_prompt = {"role":"assistant","1":"a1","2":"b1","3":"c1"}
    system_prompt = {"role":"system","1":"a2","2":"b2","3":"c2"}
    image_path = {}

    print(create_a_request(user_prompt, assistant_prompt, system_prompt, image_path))
