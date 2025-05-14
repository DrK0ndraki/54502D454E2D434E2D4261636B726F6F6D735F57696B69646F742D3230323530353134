import os
import re
from datetime import datetime
import shutil

# 定义需要查找和替换的模式
# sib9 注：如果还需要替换其他代码，仿照下面的已有规则添加即可
patterns = {
    r'\[\[include :backrooms-wiki:theme:(.*?)\]\]': r'[[include :backrooms-wiki-cn:theme:\1]]',
    r'\[\[include :backrooms-wiki:component:level-class.*?\]\]': r'[[include :backrooms-wiki-cn:component:level-class]',
    r'\[\[include :backrooms-wiki:component:license-box( [^]]*)?\]\]': r'[[include :backrooms-wiki-cn:component:license-box\1]]',
    r'\[\[include :backrooms-wiki:component:license-box-end( [^]]*)?\]\]': r'[[include :backrooms-wiki-cn:component:license-box-end\1]]',
    r'\[\[include :backrooms-wiki:component:offset-timeline([^]]*)?\]\]': r'[[include :backrooms-wiki-cn:component:offset-timeline\1]]',
    r'\[\[include :backrooms-wiki:component:open( [^]]*)?\]\]': r'[[include :backrooms-wiki-cn:credit:start\1]]',
    r'\[\[include :backrooms-wiki:component:close( [^]]*)?\]\]': r'[[include :backrooms-wiki-cn:credit:end\1]]'
}

def find_files_with_pattern(directory, extensions, patterns):
    """ 查找包含指定模式的所有文件 """
    found_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ext) for ext in extensions):
            filepath = os.path.join(directory, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # 检查是否至少匹配一个模式
                if any(re.search(pattern, content) for pattern in patterns.keys()):
                    found_files.append(filepath)
    return found_files

def replace_patterns_in_file(file_path, patterns):
    """ 在文件中替换指定模式 """
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        for old, new in patterns.items():
            content = re.sub(old, new, content)
        file.seek(0)
        file.write(content)
        file.truncate()

def create_backup(files, backup_dir=None):
    """ 创建文件备份 """
    if not backup_dir:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_dir = os.path.join('backup', now)
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    for file in files:
        shutil.copy2(file, backup_dir)

def main():
    # 获取当前目录下的相关文件
    current_directory = os.getcwd()
    files_to_process = find_files_with_pattern(current_directory, ['.ftml', '.wikidot'], patterns)
    
    print("以下文件包含可替换的Wikidot代码：")
    for file in files_to_process:
        print(file)
    
    if not files_to_process:
        print("没有找到需要替换的文件。")
        return
    
    # 询问用户是否进行替换
    confirm_replace = input("是否替换这些文件中的代码？请输入大写的YES确认：")
    if confirm_replace != "YES":
        print("取消替换操作。")
        return
    
    # 询问用户是否创建备份
    make_backup = input("是否创建文件备份？(y/n，默认为y)：").strip().lower() or 'y'
    if make_backup == 'y':
        if os.path.exists('backup'):
            use_existing = input("已存在名为'backup'的文件夹，是否使用它？(y/n)：").strip().lower()
            if use_existing != 'y':
                backup_name = input("请输入新的备份文件夹名称：")
                backup_folder = os.path.join(current_directory, backup_name)
                create_backup(files_to_process, backup_folder)
            else:
                create_backup(files_to_process)
        else:
            create_backup(files_to_process)
    
    # 执行替换
    for file in files_to_process:
        replace_patterns_in_file(file, patterns)
    
    print("替换完成！")

if __name__ == "__main__":
    main()
