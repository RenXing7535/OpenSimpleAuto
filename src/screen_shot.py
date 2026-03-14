from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageGrab

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