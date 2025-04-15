from PIL import Image
import pillow_avif
import cv2
import os

def extract_frames_from_videos(input_folder, output_folder, frame_interval=1):
    """
    从文件夹中的所有 MP4 视频提取图片帧并保存到指定文件夹。
    
    :param input_folder: 包含 MP4 视频的输入文件夹
    :param output_folder: 保存提取图片帧的输出文件夹
    :param frame_interval: 每隔多少帧提取一张图片，默认为 1（每帧都提取）
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            video_name = os.path.splitext(filename)[0]
            video_output_folder = os.path.join(output_folder, video_name)

            # 为每个视频单独创建文件夹保存帧
            os.makedirs(video_output_folder, exist_ok=True)

            # 打开视频文件
            video_capture = cv2.VideoCapture(video_path)
            if not video_capture.isOpened():
                print(f"无法打开视频文件: {video_path}")
                continue

            # 获取视频信息
            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(video_capture.get(cv2.CAP_PROP_FPS))
            print(f"处理视频: {filename} - 总帧数: {total_frames}, 帧率: {fps}")

            frame_count = 0
            saved_count = 0

            while True:
                # 读取一帧
                ret, frame = video_capture.read()
                if not ret:
                    break

                # 判断是否需要保存当前帧
                if frame_count % frame_interval == 0:
                    output_path = os.path.join(video_output_folder, f"frame_{video_name:08}_{frame_count:06d}.jpg")
                    cv2.imwrite(output_path, frame)  # 保存图片
                    saved_count += 1

                frame_count += 1

            video_capture.release()
            print(f"完成视频 {filename}: 共保存 {saved_count} 张图片到 {video_output_folder}")

def convert_jfif_to_jpeg(input_folder, output_folder, intput_extension, output_extension):
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(intput_extension):  # 检查文件扩展名是否为 .jfif
            # 构建输入文件的完整路径
            input_path = os.path.join(input_folder, filename)
            
            # 打开 .jfif 文件
            print(input_path)
            with Image.open(input_path) as img:
                # 构建输出文件的完整路径，替换扩展名为 .jpeg
                output_filename = os.path.splitext(filename)[0] + output_extension
                output_path = os.path.join(output_folder, output_filename)
                
                # 将图像保存为 .jpeg 格式
                if(output_extension == ".jpeg"):
                    img.convert("RGB").save(output_path, "JPEG")
                elif(output_extension == ".png"):
                    img.convert("RGB").save(output_path, "PNG")
                print(f"Converted: {input_path} -> {output_path}")

if __name__ == "__main__":
    input_folder = "input"  # 文件路径
    output_folder = "output"  # 替换为保存图片的文件夹路径
    frame_interval = 10  # 每隔 30 帧提取一张图片

    convert_jfif_to_jpeg(input_folder, output_folder, ".avif", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".image", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".jfif", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".jpg", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".png", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".webp", ".jpeg")
    convert_jfif_to_jpeg(input_folder, output_folder, ".heic", ".jpeg")

    #convert_jfif_to_jpeg(input_folder, output_folder, ".jpg", ".png")

    #extract_frames_from_videos(input_folder, output_folder, frame_interval)
