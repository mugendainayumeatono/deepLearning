import os
from PIL import Image
from pkg_resources import parse_version

if parse_version(Image.__version__)>=parse_version('10.0.0'):
    Image.ANTIALIAS=Image.LANCZOS

def process_image(image_path, output_path, target_width, target_height):
    """对图像进行缩放和裁剪处理"""
    img = Image.open(image_path)
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    target_aspect_ratio = target_width / target_height

    if aspect_ratio > target_aspect_ratio:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)

    img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2
    img_cropped = img_resized.crop((left, top, right, bottom))
    img_cropped.save(output_path)

def process_folder(input_folder, output_folder, target_width, target_height):
    """循环处理指定文件夹下的所有图片文件"""
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 仅处理文件（忽略子文件夹）
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path):
            # 获取输出文件的路径
            output_path = os.path.join(output_folder, filename)
            # 对图像进行处理
            process_image(input_path, output_path, target_width, target_height)
            print(f"Processed: {filename}")

# 使用示例
input_folder = 'input'  # 输入图片文件夹路径
output_folder = 'output'  # 输出图片文件夹路径
target_width = 480  # 目标宽度
target_height = 720  # 目标高度

process_folder(input_folder, output_folder, target_width, target_height)