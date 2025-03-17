import os
from PIL import Image
from pkg_resources import parse_version

if parse_version(Image.__version__)>=parse_version('10.0.0'):
    Image.ANTIALIAS=Image.LANCZOS

def resize_image(input_path, output_path, base_width=None, base_height=None):
    """
    根据指定宽度或高度，保持图片长宽比进行缩放。

    :param input_path: 输入图片路径
    :param output_path: 输出图片路径
    :param base_width: 目标宽度，传入此值时根据长宽比计算目标高度
    :param base_height: 目标高度，传入此值时根据长宽比计算目标宽度
    """
    try:
        # 打开图片
        img = Image.open(input_path)
        
        # 获取图片的原始尺寸
        original_width, original_height = img.size

        # 如果指定了宽度，根据长宽比计算高度
        if base_width is not None:
            aspect_ratio = original_height / original_width
            base_height = int(base_width * aspect_ratio)
        
        # 如果指定了高度，根据长宽比计算宽度
        elif base_height is not None:
            aspect_ratio = original_width / original_height
            base_width = int(base_height * aspect_ratio)
        
        # 调整图片大小
        img_resized = img.resize((base_width, base_height), Image.ANTIALIAS)
        
        # 保存缩放后的图片
        img_resized.save(output_path)
        print(f"图片已缩放并保存到: {output_path}")
    
    except Exception as e:
        print(f"处理图片时出错: {e}")

def resize_images_in_directory(input_directory, output_directory, base_width=None, base_height=None):
    """
    批量处理指定目录下的所有图片，按给定宽度或高度进行缩放。

    :param input_directory: 输入文件夹路径，包含所有图片
    :param output_directory: 输出文件夹路径，用于保存缩放后的图片
    :param base_width: 目标宽度
    :param base_height: 目标高度
    """
    # 如果输出文件夹不存在，创建它
    os.makedirs(output_directory, exist_ok=True)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_directory):
        input_path = os.path.join(input_directory, filename)
        
        # 确保是文件且为图片格式（可以根据需要扩展更多支持的图片格式）
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            output_path = os.path.join(output_directory, filename)
            print(f"正在处理图片: {input_path}")

            # 调用缩放函数
            resize_image(input_path, output_path, base_width=base_width, base_height=base_height)

# 示例用法
input_directory = "input"  # 替换为你的输入文件夹路径
output_directory = "output"  # 替换为你的输出文件夹路径

# 示例1：指定目标宽度，保持长宽比
#resize_images_in_directory(input_directory, output_directory, base_width=800)

# 示例2：指定目标高度，保持长宽比
resize_images_in_directory(input_directory, output_directory, base_height=720)
