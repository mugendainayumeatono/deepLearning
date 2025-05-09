import os
import win32com.client

def convert_doc_to_docx(input_folder, output_folder):
    """递归将 DOC 文件转换为 DOCX 文件，并删除原始文件"""
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  # 不显示 Word 界面
    
    for root, _, files in os.walk(input_folder):
        # 计算相对路径并在输出文件夹中创建相同的子文件夹结构
        rel_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, rel_path)
        if not os.path.exists(current_output_folder):
            os.makedirs(current_output_folder)
        
        for filename in files:
            if filename.endswith(".doc") and not filename.startswith("~$"):
                doc_path = os.path.join(root, filename)
                docx_filename = os.path.splitext(filename)[0] + ".docx"
                docx_path = os.path.join(current_output_folder, docx_filename)
                try:
                    print(f"开始转换: {doc_path} -> {docx_path}")
                    doc = word.Documents.Open(doc_path)
                    doc.SaveAs(docx_path, FileFormat=16)  # 16 表示 DOCX 格式
                    doc.Close()
                    # 确认转换成功后删除原始文件
                    if os.path.exists(docx_path):
                        os.remove(doc_path)
                        print(f"已转换并删除: {doc_path} -> {docx_path}")
                    else:
                        print(f"转换失败，未删除原始文件: {doc_path}")
                except Exception as e:
                    print(f"转换失败，未删除原始文件 {doc_path}: {str(e)}")
    
    word.Quit()

def convert_xls_to_xlsx(input_folder, output_folder):
    """递归将 XLS 文件转换为 XLSX 文件，并删除原始文件"""
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # 不显示 Excel 界面
    excel.DisplayAlerts = False  # 禁用警告提示
    
    for root, _, files in os.walk(input_folder):
        # 计算相对路径并在输出文件夹中创建相同的子文件夹结构
        rel_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, rel_path)
        if not os.path.exists(current_output_folder):
            os.makedirs(current_output_folder)
        
        for filename in files:
            if filename.endswith(".xls") and not filename.startswith("~$"):
                xls_path = os.path.join(root, filename)
                xlsx_filename = os.path.splitext(filename)[0] + ".xlsx"
                xlsx_path = os.path.join(current_output_folder, xlsx_filename)
                try:
                    wb = excel.Workbooks.Open(xls_path)
                    wb.SaveAs(xlsx_path, FileFormat=51)  # 51 表示 XLSX 格式
                    wb.Close()
                    # 确认转换成功后删除原始文件
                    if os.path.exists(xlsx_path):
                        os.remove(xls_path)
                        print(f"已转换并删除: {xls_path} -> {xlsx_path}")
                    else:
                        print(f"转换失败，未删除原始文件: {xls_path}")
                except Exception as e:
                    print(f"转换失败，未删除原始文件 {xls_path}: {str(e)}")
    
    excel.Quit()

def convert_ppt_to_pptx(input_folder, output_folder):
    """递归将 PPT 文件转换为 PPTX 文件，并删除原始文件"""
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    #powerpoint.Visible = False  # 不显示 PowerPoint 界面
    
    for root, _, files in os.walk(input_folder):
        # 计算相对路径并在输出文件夹中创建相同的子文件夹结构
        rel_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, rel_path)
        if not os.path.exists(current_output_folder):
            os.makedirs(current_output_folder)
        
        for filename in files:
            if filename.endswith(".ppt") and not filename.startswith("~$"):
                ppt_path = os.path.join(root, filename)
                pptx_filename = os.path.splitext(filename)[0] + ".pptx"
                pptx_path = os.path.join(current_output_folder, pptx_filename)
                try:
                    pres = powerpoint.Presentations.Open(ppt_path)
                    pres.SaveAs(pptx_path, FileFormat=24)  # 24 表示 PPTX 格式
                    pres.Close()
                    # 确认转换成功后删除原始文件
                    if os.path.exists(pptx_path):
                        os.remove(ppt_path)
                        print(f"已转换并删除: {ppt_path} -> {pptx_path}")
                    else:
                        print(f"转换失败，未删除原始文件: {ppt_path}")
                except Exception as e:
                    print(f"转换失败，未删除原始文件 {ppt_path}: {str(e)}")
    
    powerpoint.Quit()

def main():
    # 输入和输出文件夹路径（支持相对路径）
    input_folder = r"input"  # 相对路径，基于脚本运行时的当前工作目录
    output_folder = r"input"  # 相对路径，基于脚本运行时的当前工作目录
    
    # 转换为绝对路径以确保兼容性
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    
    # 转换 DOC 到 DOCX
    print("开始转换 DOC 文件...")
    convert_doc_to_docx(input_folder, output_folder)
    
    # 转换 XLS 到 XLSX
    print("开始转换 XLS 文件...")
    convert_xls_to_xlsx(input_folder, output_folder)
    
    # 转换 PPT 到 PPTX
    print("开始转换 PPT 文件...")
    convert_ppt_to_pptx(input_folder, output_folder)
    
    print("所有转换完成！")

if __name__ == "__main__":
    main()