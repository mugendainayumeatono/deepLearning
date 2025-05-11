import os
import comtypes.client
import pythoncom
import time
from pathlib import Path
import threading
import logging
from queue import Queue
import random

# 配置日志
logging.basicConfig(
    filename='timeout_files.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialize_com():
    """初始化COM环境"""
    try:
        pythoncom.CoInitialize()
    except Exception as e:
        print(f"COM初始化失败: {e}")

def uninitialize_com():
    """清理COM环境"""
    try:
        pythoncom.CoUninitialize()
    except Exception as e:
        print(f"COM清理失败: {e}")

def convert_doc_to_docx(input_path, output_path, result_queue):
    """将doc转换为docx"""
    initialize_com()
    word = None
    doc = None
    try:
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = True
        word.DisplayAlerts = False
        doc = word.Documents.Open(str(input_path), ReadOnly=True)
        doc.SaveAs(str(output_path), FileFormat=16)
        result_queue.put(True)
    except Exception as e:
        print(f"转换 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if doc:
                doc.Close(SaveChanges=False)
            if word:
                word.Quit()
        except Exception as e:
            print(f"关闭 Word 时出错: {e}")
        uninitialize_com()

def convert_xls_to_xlsx(input_path, output_path, result_queue):
    """将xls转换为xlsx"""
    initialize_com()
    excel = None
    wb = None
    try:
        excel = comtypes.client.CreateObject('Excel.Application')
        excel.Visible = True
        excel.DisplayAlerts = False
        wb = excel.Workbooks.Open(str(input_path), ReadOnly=True)
        wb.SaveAs(str(output_path), FileFormat=51)
        result_queue.put(True)
    except Exception as e:
        print(f"转换 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if wb:
                wb.Close(SaveChanges=False)
            if excel:
                excel.Quit()
        except Exception as e:
            print(f"关闭 Excel 时出错: {e}")
        uninitialize_com()

def convert_ppt_to_pptx(input_path, output_path, result_queue):
    """将ppt转换为pptx"""
    initialize_com()
    powerpoint = None
    pres = None
    try:
        powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
        powerpoint.Visible = True
        powerpoint.DisplayAlerts = False
        pres = powerpoint.Presentations.Open(str(input_path), ReadOnly=True, WithWindow=False)
        pres.SaveAs(str(output_path), FileFormat=24)
        result_queue.put(True)
    except Exception as e:
        print(f"转换 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if pres:
                pres.Close()
            if powerpoint:
                powerpoint.Quit()
        except Exception as e:
            print(f"关闭 PowerPoint 时出错: {e}")
        uninitialize_com()

def resave_docx(input_path, output_path, result_queue):
    """重新保存docx"""
    initialize_com()
    word = None
    doc = None
    try:
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = True
        word.DisplayAlerts = False
        doc = word.Documents.Open(str(input_path), ReadOnly=True)
        doc.SaveAs(str(output_path), FileFormat=16)
        result_queue.put(True)
    except Exception as e:
        print(f"重新保存 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if doc:
                doc.Close(SaveChanges=False)
            if word:
                word.Quit()
        except Exception as e:
            print(f"关闭 Word 时出错: {e}")
        uninitialize_com()

def resave_xlsx(input_path, output_path, result_queue):
    """重新保存xlsx"""
    initialize_com()
    excel = None
    wb = None
    try:
        excel = comtypes.client.CreateObject('Excel.Application')
        excel.Visible = True
        excel.DisplayAlerts = False
        wb = excel.Workbooks.Open(str(input_path), ReadOnly=True)
        wb.SaveAs(str(output_path), FileFormat=51)
        result_queue.put(True)
    except Exception as e:
        print(f"重新保存 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if wb:
                wb.Close(SaveChanges=False)
            if excel:
                excel.Quit()
        except Exception as e:
            print(f"关闭 Excel 时出错: {e}")
        uninitialize_com()

def resave_pptx(input_path, output_path, result_queue):
    """重新保存pptx"""
    initialize_com()
    powerpoint = None
    pres = None
    try:
        powerpoint = comtypes.client.CreateObject('PowerPoint.Application')
        powerpoint.Visible = True
        powerpoint.DisplayAlerts = False
        pres = powerpoint.Presentations.Open(str(input_path), ReadOnly=True, WithWindow=False)
        pres.SaveAs(str(output_path), FileFormat=24)
        result_queue.put(True)
    except Exception as e:
        print(f"重新保存 {input_path} 时出错: {e}")
        result_queue.put(False)
    finally:
        try:
            if pres:
                pres.Close()
            if powerpoint:
                powerpoint.Quit()
        except Exception as e:
            print(f"关闭 PowerPoint 时出错: {e}")
        uninitialize_com()

def run_with_timeout(func, args, timeout=3):
    """在指定超时时间内运行函数"""
    result_queue = Queue()
    thread = threading.Thread(target=func, args=(*args, result_queue))
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        return False, "操作超时"
    else:
        result = result_queue.get()
        return result, None

def process_file(input_path, output_dir, timeout=3):
    """处理单个文件"""
    try:
        input_path = Path(input_path).absolute()
        output_dir = Path(output_dir).absolute()
        
        file_ext = input_path.suffix.lower()
        file_name = input_path.stem
        
        # 生成4位随机数
        random_suffix = random.randint(1000, 9999)
        
        # 根据文件扩展名确定子文件夹和输出路径
        if file_ext in ('.doc', '.docx'):
            sub_dir = output_dir / 'docx_files'
            output_path = sub_dir / f"{file_name}_{random_suffix}.docx"
            func = convert_doc_to_docx if file_ext == '.doc' else resave_docx
        elif file_ext in ('.xls', '.xlsx'):
            sub_dir = output_dir / 'xlsx_files'
            output_path = sub_dir / f"{file_name}_{random_suffix}.xlsx"
            func = convert_xls_to_xlsx if file_ext == '.xls' else resave_xlsx
        elif file_ext in ('.ppt', '.pptx'):
            sub_dir = output_dir / 'pptx_files'
            output_path = sub_dir / f"{file_name}_{random_suffix}.pptx"
            func = convert_ppt_to_pptx if file_ext == '.ppt' else resave_pptx
        else:
            print(f"不支持的文件格式: {file_ext}")
            return

        # 创建子文件夹
        sub_dir.mkdir(parents=True, exist_ok=True)
        
        # 执行转换或重新保存
        success, error = run_with_timeout(func, (input_path, output_path), timeout)
        
        if not success:
            logging.info(f"文件超时或失败: {input_path}, 错误: {error}")
            print(f"处理 {input_path} 失败: {error}")
        else:
            print(f"处理 {input_path} 成功，保存到 {output_path}")
    except Exception as e:
        logging.info(f"处理文件 {input_path} 时发生未预期错误: {e}")
        print(f"处理 {input_path} 时发生未预期错误: {e}")
    finally:
        print(f"继续处理下一个文件")

def main(input_dir, output_dir, timeout=3):
    """主函数，递归处理目录中的所有office文件，跳过~$开头的文件"""
    input_dir = Path(input_dir).absolute()
    output_dir = Path(output_dir).absolute()
    
    # 支持的扩展名
    supported_extensions = {'.doc', '.xls', '.ppt', '.docx', '.xlsx', '.pptx'}
    
    # 递归遍历输入目录
    print(f"开始递归处理文件夹: {input_dir}")
    try:
        for file_path in input_dir.rglob('*'):
            try:
                if file_path.is_file():
                    if file_path.name.startswith('~$'):
                        print(f"跳过临时文件: {file_path}")
                        continue
                    if file_path.suffix.lower() in supported_extensions:
                        print(f"正在处理文件: {file_path}")
                        process_file(file_path, output_dir, timeout)
                        time.sleep(1)  # 防止COM对象未完全释放
                elif file_path.is_dir():
                    print(f"发现子文件夹: {file_path}")
            except Exception as e:
                logging.info(f"遍历文件 {file_path} 时出错: {e}")
                print(f"遍历文件 {file_path} 时出错: {e}, 继续处理下一个文件")
    except Exception as e:
        logging.info(f"遍历目录 {input_dir} 时发生未预期错误: {e}")
        print(f"遍历目录 {input_dir} 时发生未预期错误: {e}, 程序继续运行")

if __name__ == "__main__":
    # 示例用法
    input_directory = r"D:\AiDraw\resource\ppt"  # 输入文件夹
    output_directory = r"D:\AiDraw\resource\弱电资源-预处理3"  # 输出文件夹
    main(input_directory, output_directory, timeout=20)