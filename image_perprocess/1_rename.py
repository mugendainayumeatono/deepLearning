import os

def rename_files_in_folder(folder_path, prefix="file", extension=None):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    
    # 筛选出文件，不包括子文件夹
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    
    # 对文件进行重命名
    for index, file in enumerate(files, start=1):
        # 获取文件扩展名
        file_extension = os.path.splitext(file)[1]
        
        # 创建新的文件名
        new_name = f"{prefix}_{index}{extension if extension else file_extension}"
        
        # 获取原文件路径和新文件路径
        old_path = os.path.join(folder_path, file)
        new_path = os.path.join(folder_path, new_name)
        
        # 重命名文件
        os.rename(old_path, new_path)
        print(f"Renamed: {file} -> {new_name}")

if __name__ == "__main__":
    folder_path = "input"  # 替换成你的文件夹路径
    name1 = "image"
    name2 = "video"
    rename_files_in_folder(folder_path, prefix=name1)