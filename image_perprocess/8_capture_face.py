import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os
from pathlib import Path

# 初始化 InsightFace 的 FaceAnalysis 应用
#app = FaceAnalysis(providers=['CPUExecutionProvider'])  # 如果有 GPU，可以用 'CUDAExecutionProvider'
app = FaceAnalysis(providers=['CUDAExecutionProvider'])  # 如果有 GPU，可以用 'CUDAExecutionProvider'
app.prepare(ctx_id=0, det_size=(640, 640))  # 设置检测输入尺寸

# 指定输入和输出文件夹
input_folder = "input"  # 替换为你的输入文件夹路径
output_folder = "output"  # 替换为你的输出文件夹路径

# 创建输出文件夹（如果不存在）
Path(output_folder).mkdir(parents=True, exist_ok=True)

# 支持的图片扩展名
image_extensions = (".jpg", ".jpeg", ".png", ".bmp")

# 处理文件夹中的所有图片
for filename in os.listdir(input_folder):
    if filename.lower().endswith(image_extensions):
        # 构建图片完整路径
        image_path = os.path.join(input_folder, filename)
        print(f"正在处理: {filename}")

        # 加载图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法加载图片: {filename}")
            continue
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # InsightFace 需要 RGB 格式

        # 检测人脸（使用 get 方法）
        faces = app.get(image_rgb)

        if len(faces) == 0:
            print(f"{filename} 中未检测到人脸")
        else:
            # 遍历检测到的人脸
            for i, face in enumerate(faces):
                # 获取边界框坐标
                bbox = face.bbox.astype(int)  # 注意：这里改为 face.bbox
                x1, y1, x2, y2 = bbox

                # 确保坐标在图片范围内
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(image.shape[1], x2)
                y2 = min(image.shape[0], y2)

                # 截取人脸部分
                face_image = image[y1:y2, x1:x2]

                # 生成输出文件名
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}_face_{i}.jpg"
                output_path = os.path.join(output_folder, output_filename)

                # 保存截取的人脸图片
                cv2.imwrite(output_path, face_image)
                print(f"人脸已保存为: {output_path}")

            # 可选：在原图上绘制边界框并保存
            #for face in faces:
            #    bbox = face.bbox.astype(int)  # 注意：这里改为 face.bbox
            #    x1, y1, x2, y2 = bbox
            #    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # 保存带框的原图（可选）
            #marked_output_path = os.path.join(output_folder, f"{base_name}_marked.jpg")
            #cv2.imwrite(marked_output_path, image)
            #print(f"带框的原图已保存为: {marked_output_path}")

print("所有图片处理完成！")
