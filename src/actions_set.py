import os
import pyautogui
import pyperclip
import time

"""  系统级指令表参照表：
    open_workspace # 将会默认打开全屏
    create_file:path_name # 将会默认拼接工作空间的路径
    create_file_folder:path_name  # 将会默认拼接工作空间的路径
    open_file:path_name  # 将会默认拼接工作空间的路径
    open_file_folder:path_name  # 将会默认拼接工作空间的路径
    cmd_input_and_act:action_txt

    press:key # 例如 "F11" 将会打开全屏
"""
workspace_path = "D:\\6workspace\\"

def deal_cmd_action(action_txt, workspace_path):
    def join_workspace_path(workspace_path, path_name):
        return os.path.join(workspace_path, path_name)
    txt = action_txt
    left = ""
    right = ""
    if ":" in txt:
        left = txt.split(":")[0]
        right = txt.split(":")[1]
    else:
        left = txt

    if right:
        if left == "create_file":
            right = join_workspace_path(workspace_path, right)
            os.makedirs(os.path.dirname(right), exist_ok=True)
        elif left == "create_file_folder":
            right = join_workspace_path(workspace_path, right)
            os.makedirs(right, exist_ok=True)
        elif left == "open_file":
            right = join_workspace_path(workspace_path, right)
            os.startfile(right)
        elif left == "open_file_folder":
            right = join_workspace_path(workspace_path, right)
            os.startfile(right)
        elif left == "cmd_input_and_act":
            os.startfile("cmd.exe")
            pyperclip.copy(right)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
        elif left == "press":
            pyautogui.press(right)
    if not right:
        if left == "open_workspace":
            os.startfile(workspace_path)
            time.sleep(1)
            pyautogui.press("F11")

if __name__ == "__main__":
    # 测试指令
    test_commands = [
        "open_workspace",
        "create_file_folder:test_folder", 
        "create_file:test_folder\\test.txt", 
        "open_file_folder:test_folder", 
        "open_file:test_folder\\test.txt", 
        "cmd_input_and_act:echo Hello World", 
        
    ]
    
    for cmd in test_commands:
        print(f"执行指令: {cmd}")
        deal_cmd_action(cmd, workspace_path)
        time.sleep(2)  # 等待2秒，以便观察执行效果
