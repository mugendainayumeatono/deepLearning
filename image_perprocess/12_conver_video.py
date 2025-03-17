import cv2
import os

def resize_and_crop_video(input_video_path, output_video_path, target_width, target_height):
    # 打开原视频文件
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"无法打开视频文件: {input_video_path}")
        return
    
    # 获取原视频的帧率、宽度和高度
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 计算长宽比
    original_aspect_ratio = original_width / original_height
    target_aspect_ratio = target_width / target_height
    
    # 根据长宽比调整缩放比例
    if original_aspect_ratio > target_aspect_ratio:
        # 原视频较宽，按宽度缩放并裁剪高度
        new_width = target_width
        new_height = int(target_width / original_aspect_ratio)
    else:
        # 原视频较高，按高度缩放并裁剪宽度
        new_height = target_height
        new_width = int(target_height * original_aspect_ratio)

    # 计算裁剪区域，使视频居中
    x_offset = (new_width - target_width) // 2
    y_offset = (new_height - target_height) // 2

    if new_width < target_width:
        target_width = new_width
        x_offset = 0

    if new_height < target_height:
        target_height = new_height
        y_offset = 0
    
    # 创建视频写入器，使用裁剪后的尺寸
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 格式
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (target_width, target_height))
    
    # 检查视频写入器是否打开成功
    if not out.isOpened():
        print(f"无法创建视频文件: {output_video_path}")
        cap.release()
        return
    
    # 处理视频帧
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 缩放视频帧
        resized_frame = cv2.resize(frame, (new_width, new_height))
        
        # 裁剪视频帧，保证居中
        cropped_frame = resized_frame[y_offset:y_offset+target_height, x_offset:x_offset+target_width]
        
        # 写入新的视频帧
        out.write(cropped_frame)
    
    # 释放资源
    cap.release()
    out.release()

    print(f"视频已缩放并裁剪为指定分辨率，保存为 {output_video_path}")

def change_fps(input_video_path, output_video_path, target_fps=8):
    # 打开原视频文件
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"无法打开视频文件: {input_video_path}")
        return
    
    # 获取原视频的帧率、宽度和高度
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 计算跳过多少帧来达到目标帧率
    frame_skip = int(original_fps // target_fps)
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 格式
    out = cv2.VideoWriter(output_video_path, fourcc, target_fps, (width, height))
    
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 如果当前帧数是需要保留的帧（每隔frame_skip帧保存一帧）
        if frame_count % frame_skip == 0:
            out.write(frame)
        
        frame_count += 1
    
    # 释放资源
    cap.release()
    out.release()

    print(f"视频已转换为 {target_fps} FPS，保存为 {output_video_path}")

def split_video(input_video_path, frame_count_per_segment, output_folder):
    # 打开视频文件
    cap = cv2.VideoCapture(input_video_path)
    
    if not cap.isOpened():
        print(f"无法打开视频文件: {input_video_path}")
        return
    
    # 获取视频的帧率、宽度和高度
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 计算要切分成多少个片段
    num_segments = total_frames // frame_count_per_segment + (1 if total_frames % frame_count_per_segment != 0 else 0)

    segment_index = 0
    frame_count = 0
    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 如果已经读取了指定的帧数，保存当前片段并开始新的片段
        if frame_count % frame_count_per_segment == 0:
            if out is not None:
                out.release()  # 释放之前的片段
            # 创建新的片段输出视频文件
            segment_index += 1
            output_video_path = os.path.join(output_folder, os.path.splitext(os.path.basename(input_video_path))[0] + f"_segment_{segment_index}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4 格式
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
        
        # 写入当前帧到当前片段视频文件
        out.write(frame)
        frame_count += 1
    
    # 释放资源
    cap.release()
    if out is not None:
        out.release()

    print(f"视频切割完毕，共切割为 {segment_index} 个片段。")

def process_videos_in_folder(folder_path, output_folder, target_width, target_height, target_fps, frame_count_per_segment):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 如果文件是视频文件（可以根据扩展名判断）
        if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            temp_resize_video_path = os.path.join(output_folder, os.path.splitext(filename)[0] + f"_resized_{target_width}x{target_height}_fps_{target_fps}.mp4")
            
            # Step 1: Resize and crop video
            resize_and_crop_video(file_path, temp_resize_video_path, target_width, target_height)
            
            # Step 2: Change FPS
            temp_fps_video_path = os.path.join(output_folder, os.path.splitext(filename)[0] + f"_temp_fps.mp4")
            change_fps(temp_resize_video_path, temp_fps_video_path, target_fps)
            
            # Step 3: Split video into segments
            split_video(temp_fps_video_path, frame_count_per_segment, output_folder)

            # 删除中间产物（临时帧率调整后的文件）
            if os.path.exists(temp_resize_video_path):
                os.remove(temp_resize_video_path)
                print(f"已删除临时文件: {temp_resize_video_path}")

            # 删除中间产物（临时帧率调整后的文件）
            if os.path.exists(temp_fps_video_path):
                os.remove(temp_fps_video_path)
                print(f"已删除临时文件: {temp_fps_video_path}")

# 使用示例
folder_path = "input"  # 替换成你的输入文件夹路径
output_folder = "output"  # 替换成你想要保存输出文件的文件夹路径
target_width = 480  # 目标宽度
target_height = 720  # 目标高度
target_fps = 8  # 目标帧率
frame_count_per_segment = 49  # 每个片段的帧数
process_videos_in_folder(folder_path, output_folder, target_width, target_height, target_fps, frame_count_per_segment)
