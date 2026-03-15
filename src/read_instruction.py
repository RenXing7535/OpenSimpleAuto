
# 下面是关于回复处理的代码
"""
    |<head>["思考内容","增加的记忆片段"]
    |<type1>["(横坐标相对于图片长度的比例,纵坐标相对于图片宽度的比例)","LEFT/RIGHT"]
    |<type2>["滑动的大小"]
    |<type3>["输入内容"]
    |<type4>["等待时间"]
    |<type5>["BackSpace删除,要求是整数"]
    |<type6>["这里需要填入一个系统级指令的名称,具体你要参考指令表"]
    |<final>["True/False"]
    <type>可以自由组合排列
    <final>必须在最后一个指令，用于决定下一轮操作获取到什么内容
    """

def deal_actions(actions):
    print(actions)
    num = len(actions)
    results = []
    for i in range(num):
        aim_text = actions[i]
        print("deal_text:",aim_text)
        txt_head = aim_text[0:7]
        text_content = aim_text[7:]
        text_splite = text_content.split('"')
        pre_remove_index = []
        for i in range(len(text_splite)):
            if text_splite[i] == "" or text_splite[i] == " " or text_splite[i] == "," or text_splite[i] == "[" or text_splite[i] == "]":
                pre_remove_index.append(i)
        for i in range(len(pre_remove_index)):
            text_splite.pop(pre_remove_index[i]-i)
        result = None
        if txt_head == "<type1>":
            position = text_splite[0]
            click_type = text_splite[0]
            result = {"type":txt_head,"position":position,"click_type":click_type}
        elif txt_head == "<type2>":
            slide_size = text_splite[0]
            result = {"type":txt_head,"slide_size":slide_size}
        elif txt_head == "<type3>":
            input_text = text_splite[0]
            result = {"type":txt_head,"input_text":input_text}
        elif txt_head == "<type4>":
            wait_time = text_splite[0]
            result = {"type":txt_head,"wait_time":wait_time}
        elif txt_head == "<final>":
            final = text_splite[0]
            result = {"type":txt_head,"final":bool(final)}
        elif txt_head == "<type5>":
            backspace_num = text_splite[0]
            result = {"type":txt_head,"backspace_num":int(backspace_num)}
        elif txt_head == "<type6>":
            system_cmd = text_splite[0]
            result = {"type":txt_head,"system_cmd":system_cmd}
        results.append(result)
    return results
# 
def deal_head(head_text:str):
    text = head_text.replace("<head>","").replace("[","").replace("]","").replace('"',"")
    tem_str = ""
    result = []
    for i in text:
        if i != ',':
            tem_str += i
        if i == ',':
            result.append(tem_str)
            tem_str = ''
        if i == text[-1]:
            result.append(tem_str)
            tem_str = ''
    result = {"thought":result[0],"memory":result[1]}
    print("<head>:",result)
    return result

# 
def for_text(list):
    for i in range(len(list)):
        print(list[i])
# 
def deal_response(aim_text):
    if ' ' in aim_text:
        aim_text = aim_text.replace(' ','')
    aim_text = aim_text.split("|")
    del aim_text[0]
    thought_memory = aim_text.pop(0)
    actions = aim_text[1:]
    actions = deal_actions(actions)
    thought_memory = deal_head(thought_memory)
    del aim_text
    return {"thought_memory":thought_memory,"actions":actions}
# 
