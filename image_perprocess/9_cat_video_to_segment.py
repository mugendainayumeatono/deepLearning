import cv2
import os

def split_video_by_frames(input_video, frames_per_segment, output_dir="output", txt_content="This is a segment"):
    """
    将单个视频按指定帧数分割成多个短视频，并为每个片段生成同名txt文件
    输出文件名包含原视频文件名
    
    参数:
    input_video (str): 输入视频文件路径
    frames_per_segment (int): 每个短视频的帧数
    output_dir (str): 输出目录
    txt_content (str): 要写入txt文件的内容
    """
    # 创建视频特定的输出目录（使用原文件名作为子目录）
    video_name = os.path.splitext(os.path.basename(input_video))[0]
    video_output_dir = os.path.join(output_dir, video_name)
    if not os.path.exists(video_output_dir):
        os.makedirs(video_output_dir)
    
    # 打开视频文件
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"错误：无法打开视频文件 {input_video}")
        return
    
    # 获取视频属性
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"处理 {input_video}: 总帧数 {total_frames}, 帧率 {fps}")
    
    # 计算需要分割成多少个片段
    num_segments = (total_frames + frames_per_segment - 1) // frames_per_segment
    
    # 当前处理的帧计数器
    frame_count = 0
    segment_count = 0
    writer = None
    
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            break  # 视频结束
        
        # 如果需要开始新的片段
        if frame_count % frames_per_segment == 0:
            # 关闭上一个 writer（如果存在）
            if writer is not None:
                writer.release()
            
            # 创建新的视频写入器，文件名包含原视频名
            segment_count += 1
            output_file = os.path.join(video_output_dir, f"{video_name}_segment_{segment_count}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 编码
            writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            print(f"生成视频: {output_file}")
            
            # 生成同名txt文件
            txt_file = os.path.join(video_output_dir, f"{video_name}_segment_{segment_count}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            print(f"生成文本: {txt_file}")
        
        # 写入当前帧
        writer.write(frame)
        frame_count += 1
    
    # 释放资源
    if writer is not None:
        writer.release()
    cap.release()
    
    print(f"{input_video} 分割完成，共生成 {segment_count} 个片段")

def process_directory(input_dir, frames_per_segment, output_dir="output", txt_content="This is a segment"):
    """
    处理指定目录下的所有视频文件
    
    参数:
    input_dir (str): 输入目录路径
    frames_per_segment (int): 每个短视频的帧数
    output_dir (str): 输出目录
    txt_content (str): 要写入txt文件的内容
    """
    # 支持的视频文件扩展名
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')
    
    # 遍历目录中的所有文件
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(video_extensions):
                input_video = os.path.join(root, file)
                split_video_by_frames(input_video, frames_per_segment, output_dir, txt_content)

# 使用示例
if __name__ == "__main__":
    # 输入参数
    input_directory = "input"         # 包含视频的输入目录
    frames_per_seg = 57              # 每段300帧（例如30fps下为10秒）
    output_directory = "output" # 输出目录
    custom_txt_content = "yamitest"  # 自定义txt内容
    
    process_directory(input_directory, frames_per_seg, output_directory, custom_txt_content)
