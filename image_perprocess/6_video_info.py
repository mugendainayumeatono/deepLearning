import cv2
import os

def get_video_info(input_video_path):
    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"无法打开视频文件: {input_video_path}")
        return
    
    # 获取视频的长宽、帧率和总帧数
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 释放视频资源
    cap.release()
    
    # 构造输出文件路径，与输入视频同名的文本文件
    base_name = os.path.splitext(os.path.basename(input_video_path))[0]
    output_text_file = os.path.join(os.path.dirname(input_video_path), f"{base_name}_video_info.txt")
    
    # 将信息写入文本文件
    with open(output_text_file, "w") as file:
        file.write(f"视频文件: {input_video_path}\n")
        file.write(f"视频宽度: {width} 像素\n")
        file.write(f"视频高度: {height} 像素\n")
        file.write(f"帧率: {fps} 帧/秒\n")
        file.write(f"总帧数: {total_frames} 帧\n")
    
    print(f"视频信息已写入 {output_text_file}")

def process_videos_in_folder(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 如果文件是视频文件（可以根据扩展名判断）
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            get_video_info(file_path)

# 使用示例
folder_path = "input"  # 替换成你的文件夹路径
process_videos_in_folder(folder_path)
