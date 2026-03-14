import src.act_instruction as act_instruction
import src.read_instruction as read_instruction
import src.about_request as about_request
import src.clean_resource as clean_resource
import src.screen_shot as screen_shot
import src.read_env as read_env
import time
import traceback


def main():
    # 截图并保存为screen.png
    image_path = read_env.screen_path
    screen_width, screen_height = screen_shot.screen_shot(image_path)

    # 控制循环
    switch = True
    num_times = 0
    s1 = False
    s2 = False
    s3 = False

    # 记录时间
    timestart = time.time()
    timeend = 0

    # 定义一个工作流程
    def a_work_flew():
        nonlocal num_times, timeend
        num_times += 1
        print("running_times:",num_times)
        # 截屏
        screen_shot.screen_shot(image_path)
        # 处理屏幕图像
        screen_shot.deal_screen_image(image_path)
        # 读取prompt
        user_prompt = ''
        system_prompt = ''
        assistant_prompt = ''
        with open(f"{read_env.user_prompt_path}", 'r', encoding='utf-8') as file:
            user_prompt = file.read()
            file.close()
        with open(f"{read_env.system_prompt_path}", 'r', encoding='utf-8') as file:
            system_prompt = file.read()
            file.close()
        with open(f"{read_env.assistant_prompt_path}", 'r', encoding='utf-8') as file:
            assistant_prompt = file.read()
            file.close()
        # 创建资源体
        user_prompt = {"role":"user","user_prompt":user_prompt}
        assistant_prompt = {"role":"assistant","assistant_prompt":assistant_prompt}
        system_prompt = {"role":"system","system_prompt":system_prompt}
        image = {"screen_shot":image_path}
        # 创建请求
        request = about_request.create_a_request(user_prompt=user_prompt,assistant_prompt=assistant_prompt,system_prompt=system_prompt,image_path=image)
        # 发送请求
        response = about_request.send_request_get_response(request, read_env.model2_name, read_env.model2_url, read_env.API_KEY)
        # 记录历史响应
        with open(f"{read_env.history_response_path}", 'a', encoding='utf-8') as file_history:
            file_history.write(f"{num_times}:{response}\ntime:{time.time()}\n")
            file_history.close()
        # 处理响应
        result = read_instruction.deal_response(response)
        thought = result["thought"]
        actions = result["actions"]
        # 记录历史思考
        with open(f"{read_env.memory_path}", 'a', encoding='utf-8') as memory:
            memory.write(thought)
            memory.close()
        # 执行动作
        act_instruction.execute_instruction(actions,screen_width,screen_height)
        # times
        timeend = time.time()
        print("running_time:",timeend-timestart)
    def self_thought(memory_prompt):
        """这里用来对历史回复和记忆文件进行精炼总结"""
        
        with open(f"{read_env.memory_path}", 'r', encoding='utf-8') as memory:
            memory_content = memory.read()
            memory.close()
        with open(f"{read_env.history_response_path}", 'r', encoding='utf-8') as file_history:
            history_response = file_history.read()
            file_history.close()
        # 创建请求
        system_prompt = {"role":"system","system_prompt":memory_prompt}
        user_prompt = {"role":"user","user_prompt":history_response + memory_content}
        # 创建请求
        request = about_request.create_a_request(system_prompt=system_prompt,
                                                 user_prompt=user_prompt)
        # 发送请求
        response = about_request.send_request_get_response(request, read_env.model1_name, read_env.model1_url, read_env.API_KEY)
        # 记录历史思考
        with open(f"{read_env.memory_path}", 'w', encoding='utf-8') as memory:
            memory.write(response)
            memory.close()


    # 循环执行工作流程
    while switch:
        try:
            with open(f"{read_env.memory_prompt_path}", 'r', encoding='utf-8') as memory_prompt_file:
                    memory_prompt = memory_prompt_file.read()
                    memory_prompt_file.close()
            if num_times % 20 == 0:
                print("self_thought")
                self_thought(memory_prompt)
            print("a_work_flew")
            a_work_flew()
        except Exception as e:
            switch = False
            print(f"工作流程执行时出错: {e}, traceback: {traceback.format_exc()}")
    clean_resource.cleanup_resources()




if __name__ == "__main__":
    # 测试代码
    main()
