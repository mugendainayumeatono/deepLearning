from PIL import Image
import os

def mirror_images(input_folder, output_folder, flip_type="horizontal"):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 支持的图片扩展名
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    # 计数器
    processed_count = 0
    error_count = 0
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"mirrored_{filename}")
            
            try:
                # 打开图片
                image = Image.open(input_path)
                
                # 根据flip_type选择翻转方式
                if flip_type.lower() == "vertical":
                    mirrored_image = image.transpose(Image.FLIP_TOP_BOTTOM)
                else:  # 默认水平翻转
                    mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)
                
                # 保存翻转后的图片
                mirrored_image.save(output_path)
                processed_count += 1
                print(f"已处理: {filename}")
                
            except Exception as e:
                print(f"处理 {filename} 时出错: {str(e)}")
                error_count += 1
    
    # 打印总结
    print(f"\n处理完成！")
    print(f"成功处理图片数: {processed_count}")
    print(f"失败图片数: {error_count}")

# 使用示例
if __name__ == "__main__":
    # 指定输入和输出文件夹
    input_folder = "input"    # 输入图片文件夹路径
    output_folder = "output"  # 输出图片文件夹路径
    
    # 可以选择翻转类型: "horizontal"（水平） 或 "vertical"（垂直）
    mirror_images(input_folder, output_folder, flip_type="horizontal")
