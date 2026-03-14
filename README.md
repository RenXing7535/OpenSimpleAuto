# 项目名称
OpenSimpleAuto
version:test0.1

# 提示
- 1. 开发者非常喜欢干净的代码 非常不喜欢用try和except来处理异常 因为这样会使代码变得非常复杂 并且难以维护
- 2. 有什么bug当场就解决掉

# 项目介绍
- 1. 最简单的ai桌面agent
- 2. 技术栈：
    - 1.1 python
    - 1.2 openai api
    - 1.3 其他相关库：
        - 1.3.1 pyautogui
        - 1.3.2 pyperclip
        - 1.3.3 time
        - 1.3.4 datetime
        - 1.3.5 io
        - 1.3.6 dotenv
        - 1.3.7 os
        - 1.3.8 base64
        - 1.3.9 openai
        - 1.3.10 PIL
- 3. 项目结构
    - 3.1 main.py
    - 3.2 .env
    - 3.3 README.md
    - 3.4 run.py 预先准备的简单入口
# 程序结构
- 下面这个流程已经改了 改了一点点
- 流程开始: 
- 截图并保存为screen.png
- 对获取的图片进行预处理
- 向ai发送请求内容是：
    - prompt.txt
    - screen.png
- ai返回内容是：
    - 指令
    - 思考文本（对当前画面的识别思考）
    - 记忆修改
- 本地执行器对上述信息进行解析
- 通过本地执行器执行相应操作 并且保存相关记忆文件
- 循环流程

# 使用
bash python run.py/main.py

# 开发者
@THILAK 2013686371@qq.com/@T_dalt wx Renxself7535
