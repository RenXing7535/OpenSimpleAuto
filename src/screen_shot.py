from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageGrab
import uiautomation as auto
import time


def get_screen_text():
    # 任务栏
    root = auto.GetRootControl()

    def mask_find(element: auto.Control, depth=0):

        find_aim = False
        aim = None

        if not find_aim:
            for child in element.GetChildren():
                mask_find(child, depth+1)
                if child.Name == "任务栏":
                    find_aim = True
                    aim = child
        return aim
    
    def track_mask_list(contral: auto.Control):
        rect = contral.BoundingRectangle

        center = (rect.left + rect.width()//2, rect.top + rect.height()//2)

        mask_list = {
            "名称": contral.Name,
            "位置": center,
            "子元素": []
        }
        for child in contral.GetChildren():
            rect = child.BoundingRectangle
            center = (rect.left + rect.width()//2, rect.top + rect.height()//2)
            mask_list["子元素"].append({
                "名称": child.Name,
                "位置": center,
                "子元素": [ track_mask_list(child) for child in child.GetChildren() ]
            })

        return mask_list

    def tree_to_list(mask_list):
        list =[]
        def traverse(mask_list):
            if mask_list["名称"] != "":
                list.append((mask_list["名称"], mask_list["位置"]))
            for child in mask_list["子元素"]:
                traverse(child)
        traverse(mask_list)
        return list

    mask = mask_find(root)

    #print(mask)

    mask = track_mask_list(mask)
    mask = tree_to_list(mask)

    # front window
    front = auto.GetForegroundControl()
    front = track_mask_list(front)
    front = tree_to_list(front)

    #print(1,front)


    return "" f"任务栏: {mask}\n当前窗口: {front}"


if __name__ == "__main__":
    time.sleep(5)
    
    self_tree = get_screen_text()

    print(self_tree)



def get_screen_size(image_path):
    # 获取屏幕尺寸
    with Image.open(image_path) as image_file:
        width, height = image_file.size
    return width, height

def screen_shot(path="screen.png"):
    # 截图并保存为screen.png
    get_screen = ImageGrab.grab()
    get_screen.save(path)
    image_path = path
    screen_width, screen_height = get_screen_size(image_path)
    return screen_width, screen_height

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