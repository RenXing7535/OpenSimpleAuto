from dotenv import load_dotenv
import os 
import base64
from openai import OpenAI
from PIL import ImageGrab
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import pyautogui
import time
import datetime
from io import BytesIO
# 这里是关于查看屏幕的相关定义

def get_screen_size(image_path):
    # 获取屏幕尺寸
    with Image.open(image_path) as image_file:
        width, height = image_file.size
    return width, height

# 这里是关于环境变量配置还有关于模型调用的相关定义

load_dotenv()
model_name = os.getenv('DOUBAO_MODEL_NAME')
api_url = os.getenv('DOUBAO_API_URL')
api_key = os.getenv('DOUBAO_API_KEY')

def create_a_request(image_path, prompt):
    # 创建一个请求
    with open(image_path, "rb") as image_file:

        img = Image.open(image_file)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    request = [
    {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url":f"data:image/png;base64,{image_base64}"},
                "file_name": "屏幕截图.png"
            },
            {
                "type": "text",
                "text": prompt
            },
        ],
    }
    ]
    return request

def send_request_get_response(request, model_name, api_url, api_key, max_tokens=1024, temperature=0.8, top_p=0.9):
    # 发送请求并获取响应
    client = OpenAI(base_url=api_url, api_key=api_key)
    response = client.chat.completions.create(model=model_name, messages=request, stream=True, max_tokens=max_tokens, temperature=temperature, top_p=top_p)
    return response
def turn_response_to_text(response):
    # 将响应转换为文本
    text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            text += chunk.choices[0].delta.content
    print("\n文本转化程序的结果：")
    print(text)
    return text

# 下面是关于回复处理的代码

def deal_response(aim_text):
    """
    <type1>["思考内容","(横坐标相对于图片长度的比例,纵坐标相对于图片宽度的比例)","LEFT/RIGHT"]
    <type2>["思考内容","滑动的大小"]
    <type3>["思考内容","输入内容"]
    """
    if ' ' in aim_text:
        aim_text = aim_text.replace(' ','')
    txt_head = aim_text[0:7]
    print("\n",txt_head)
    text_content = aim_text[7:]
    text_splite = text_content.split('"')
    pre_remove_index = []
    for i in range(len(text_splite)):
        if text_splite[i] == "" or text_splite[i] == " " or text_splite[i] == "," or text_splite[i] == "[" or text_splite[i] == "]":
            pre_remove_index.append(i)
    for i in range(len(pre_remove_index)):
        text_splite.pop(pre_remove_index[i]-i)
    print(text_splite)
    result = None
    if txt_head == "<type1>":
        position = text_splite[1]
        click_type = text_splite[2]
        result = {"type":txt_head,"thought":text_splite[0],"position":position,"click_type":click_type}
    elif txt_head == "<type2>":
        slide_size = text_splite[1]
        result = {"type":txt_head,"thought":text_splite[0],"slide_size":slide_size}
    elif txt_head == "<type3>":
        input_text = text_splite[1]
        result = {"type":txt_head,"thought":text_splite[0],"input_text":input_text}
    try:
        return result
    except:
        print(" text_error ")
        return {"type":"<type3>","thought":"None","slide_size":0}
        
# 这里是关于指令执行的代码
def execute_instruction(instruction, screen_width, screen_height):
    # 执行指令
    #  指令类型：<type1>["思考内容","(横坐标相对于图片长度的比例,纵坐标相对于图片宽度的比例)","LEFT/RIGHT"]
    #  指令类型：<type2>["思考内容","滑动的大小"]
    #  指令类型：<type3>["思考内容","输入内容"]
    try:
        if instruction != None:
            if instruction["type"] == "<type1>":
                x, y = eval(instruction["position"])
                x = (int(x * screen_width) ) 
                y = (int(y * screen_height) )
                if instruction["click_type"] == "LEFT":
                    pyautogui.click(x, y)
                elif instruction["click_type"] == "RIGHT":
                    pyautogui.rightClick(x, y)
            elif instruction["type"] == "<type2>":
                slide_size = int(instruction["slide_size"])
                pyautogui.scroll(slide_size)
            elif instruction["type"] == "<type3>":
                input_text = instruction["input_text"]
                pyperclip.copy(input_text)
                pyautogui.hotkey('ctrl', 'v')
    except Exception as e:
        print(f"执行指令时出错: {e}")
        
# 反思

def read_prompt_from_file(file_path):
    # 从文件中读取提示词
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    return prompt

def write_prompt_to_file(prompt, file_path):
    # 将提示词写入文件
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


def create_a_request_about_self_thought(be_deal_memory, old_prompt, prompt_t):
    # 创建一个请求
    request = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_t
            },
            {
                "type": "text",
                "text": be_deal_memory
            },
            {
                "type": "text",
                "text": old_prompt
            },
        ],
    }
    ]
    return request

# main 函数
def cleanup_resources():
    # 清理资源
    try:
        if os.path.exists("image.png"):
            os.remove("image.png")
            print("已清理临时文件 image.png")
    except Exception as e:
        print(f"清理资源时出错: {e}")

def deal_screen_image(image_path):
    # 处理屏幕图像
    # 这一部分用来在截图上绘制网格并且标注一部分坐标
    font1 = ImageFont.load_default(size=20)
    
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        grid_size = width//10
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill="red")
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill="red")
        # text
        for x in range(0, width, grid_size):
            for y in range(0, height, grid_size):
                draw.text((x, y), f"({x/width},{y/height})", fill="white", font=font1)
        #
        image_out = image
    except Exception as e:
        print(f"处理图像时出错: {e}")
        image_out = None

    if image_out:
        image_out.save(image_path)
    return None

def main():
    try:
        get_screen = ImageGrab.grab()
        get_screen.save("image.png")
        image_path = "image.png"
        screen_width, screen_height = get_screen_size(image_path)

        switch = True

        timestart = time.time()
        timeend = 0

        last_response = None
        last_last_response = None

        n = 0
        n_b = 0

        history_thought = []
        with open("history_thought.txt", 'a', encoding='utf-8') as file_history:
            while switch:
                n += 1
                n_b += 1
                print("running_times:",n)
                get_screen = ImageGrab.grab()
                get_screen.save("image.png")
                deal_screen_image(image_path)
                # DEAL IMAGE

                # 
                prompt = read_prompt_from_file('prompt.txt')
                memory = read_prompt_from_file("memory.txt")
                if last_response:
                    prompt += f"last_response：{last_response}"
                    if last_last_response:
                        prompt += f"last_last_response：{last_last_response}"
                request = create_a_request(image_path, prompt + memory)
                response = send_request_get_response(request, model_name, api_url, api_key)
                text = turn_response_to_text(response)

                a_response = f"running_times:{n}\n" + f"time:{timeend - timestart}\n" + f"date:{datetime.datetime.now()}\n" + f"response:{text}\n"
                file_history.write(a_response)
                
                instruction = deal_response(text)
                last_last_response = last_response
                last_response = instruction

                execute_instruction(instruction, screen_width, screen_height)
                history_thought.append(instruction['thought'])
                # 反思
                if n_b > 50:
                    be_deal_memory = f"last_response：{instruction['thought']}"
                    prompt_t = read_prompt_from_file("self_thought_prompt.txt")
                    request = create_a_request_about_self_thought(be_deal_memory, memory, prompt_t)
                    response = send_request_get_response(request, model_name, api_url, api_key)
                    new_memory = turn_response_to_text(response)
                    write_prompt_to_file(new_memory, "memory.txt")
                    history_thought = []
                    n_b = 0
                timeend = time.time()
                print("time:",timeend - timestart)
                timestart = timeend

                #if n == 100:
                #    switch = False
    except KeyboardInterrupt:
        print("\n程序被用户中断，正在退出...")
    except Exception as e:
        print(f"程序运行出错: {e}")
    finally:
        cleanup_resources()
        print("程序已退出")


if __name__ == "__main__":
    # 测试代码
    main()
