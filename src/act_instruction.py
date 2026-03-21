import pyautogui
import pyperclip
import time
import src.read_env as read_env
import src.actions_set as actions_set

# 处理type6指令
def deal_type6(action_name):
    """  系统级指令表参照表：
    open_workspace
    create_file:path_name
    create_file_folder:path_name
    open_file:path_name
    open_file_folder:path_name
    open_a_cmd
    cmd_input_and_act:action_txt
    """
    actions_set.deal_cmd_action(action_name, read_env.workspace_path)
    pass

# 这里是关于指令执行的代码
def execute_instruction(actions, screen_width, screen_height):
    if actions != []:
        for instruction in actions:
            try:
                if instruction != "":
                    print(instruction)
                    if instruction["type"] == "<type1>":
                        x, y = eval(instruction["position"])
                        x = (int(x * screen_width) ) 
                        y = (int(y * screen_height) )
                        if instruction["click_type"] == "LEFT":
                            pyautogui.click(x, y)
                            print(f"点击了坐标 ({x}, {y})")
                        elif instruction["click_type"] == "RIGHT":
                            pyautogui.rightClick(x, y)
                            print(f"点击了坐标 ({x}, {y})")
                    elif instruction["type"] == "<type2>":
                        slide_size = int(instruction["slide_size"])
                        pyautogui.scroll(slide_size)
                    elif instruction["type"] == "<type3>":
                        input_text = instruction["input_text"]
                        pyperclip.copy(input_text)
                        pyautogui.hotkey('ctrl', 'v')
                    elif instruction["type"] == "<type4>":
                        time.sleep(instruction['wait_time'])
                    elif instruction["type"] == "<type5>":
                        backspace_num = instruction["backspace_num"]
                        for i in range(backspace_num):
                            pyautogui.press('backspace')
                    elif instruction["type"] == "<type6>":
                        system_cmd = instruction["system_cmd"]
                        deal_type6(system_cmd)
                    elif instruction["type"] == "<final>":
                        print("final:",instruction)
                # 等待0.5秒
                time.sleep(0.5)
            except Exception as e:
                print(f"执行指令时出错: {e}")
        return instruction["type"]

