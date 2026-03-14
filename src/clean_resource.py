import os
def cleanup_resources():
    """清理临时资源"""
    try:
        if os.path.exists("image.png"):
            os.remove("image.png")
            print("已清理临时文件 image.png")
        if os.path.exists("memory\history_thought.txt"):
            os.remove("memory\history_thought.txt")
            print("已清理临时文件 history_thought.txt")
            os.mknod("memory\history_thought.txt")
    except Exception as e:
        print(f"清理资源时出错: {e}")
