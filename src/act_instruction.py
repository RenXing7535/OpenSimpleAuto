import pyautogui
import pyperclip
import time

# 这里是关于指令执行的代码
def execute_instruction(actions, screen_width, screen_height):
    for instruction in actions:
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
                elif instruction["type"] == "<type4>":
                    time.sleep(instruction['wait_time'])
                elif instruction["type"] == "<final>":
                    pass
            # 等待0.5秒
            time.sleep(0.5)
        except Exception as e:
            print(f"执行指令时出错: {e}")
    return instruction["type"]