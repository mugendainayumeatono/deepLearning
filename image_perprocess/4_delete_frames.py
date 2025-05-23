import os
import cv2
def remove_first_n_frames(input_video, output_video, n_frames):
    # 打开输入视频
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("无法打开视频文件")
        return
    
    # 获取视频属性
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if n_frames >= total_frames:
        print("要删除的帧数大于视频总帧数")
        cap.release()
        return
    
    # 设置输出视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码格式
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # 跳过前 N 帧
    for _ in range(n_frames):
        cap.read()  # 读取并丢弃帧
    
    # 读取并写入剩余帧
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    # 释放资源
    cap.release()
    out.release()
    print(f"已删除前 {n_frames} 帧，输出视频保存为 {output_video}")

def remove_last_n_frames(input_video_path, output_video_path, n_frames):
    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)

    # 获取视频的帧率、总帧数、宽度和高度
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 计算需要读取的帧数（总帧数减去 N 帧）
    frames_to_read = total_frames - n_frames

    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 格式
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # 读取并写入帧
    for i in range(frames_to_read):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # 释放资源
    cap.release()
    out.release()

def remove_frames_in_directory(input_directory, output_directory, n_frames):

    # 如果输出文件夹不存在，创建它
    os.makedirs(output_directory, exist_ok=True)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(input_directory):
        input_path = os.path.join(input_directory, filename)
        
        # 确保是文件且为图片格式（可以根据需要扩展更多支持的图片格式）
        if os.path.isfile(input_path) and filename.lower().endswith(('.mp4')):
            output_path = os.path.join(output_directory, filename)
            print(f"正在处理: {input_path}")

            # 调用缩放函数
            #remove_last_n_frames(input_path, output_path, n_frames)
            remove_first_n_frames(input_path, output_path, n_frames)

# 使用示例
input_directory = "input"  # 替换为你的输入文件夹路径
output_directory = "output"  # 替换为你的输出文件夹路径
remove_framse = 32
remove_frames_in_directory(input_directory, output_directory, remove_framse) 