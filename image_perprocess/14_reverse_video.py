from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import time_mirror
import os

def reverse_video(input_path, output_path):
    # 加载视频文件
    video = VideoFileClip(input_path)
    
    # 倒放视频
    reversed_video = video.fx(time_mirror)
    
    # 保存倒放后的视频
    reversed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    # 关闭视频对象以释放资源
    video.close()
    reversed_video.close()

def reverse_videos_in_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 支持的视频文件扩展名
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(video_extensions):
            input_path = os.path.join(input_folder, filename)
            # 为输出文件生成路径，添加 '_reversed' 后缀
            output_filename = os.path.splitext(filename)[0] + '_reversed' + os.path.splitext(filename)[1]
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"Processing: {filename}")
            try:
                reverse_video(input_path, output_path)
                print(f"Successfully reversed: {output_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    input_folder = "input"  # 输入视频文件夹路径
    output_folder = "output"  # 输出视频文件夹路径
    reverse_videos_in_folder(input_folder, output_folder)