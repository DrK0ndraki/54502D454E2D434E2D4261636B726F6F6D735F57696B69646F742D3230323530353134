import os
import re

# 替换规则
REPLACEMENT_RULES = {
    'name': '名称',
    'author': '作者',
    'license': '授权协议',
    'source link': '来源链接',
    'derivative of': '衍生自',
    'additional notes': '备注',
    'filename': '文件名',
}

# 正则表达式定义
START_PATTERN = re.compile(
    r'\[\[include :backrooms-wiki-cn:component:license-box(?:\s+\w+=\S+)*\]\]'
)
END_PATTERN = re.compile(
    r'\[\[include :backrooms-wiki-cn:component:license-box-end\]\]'
)
PROJECT_LINE_PATTERN = re.compile(
    r'^>?\s*(\**)([A-Za-z\s]+)(\**)\s*:\s*(.*)$',  # 允许">"开头和更灵活的星号处理
    re.IGNORECASE
)

def find_structures(lines):
    starts = []
    ends = []
    for idx, line in enumerate(lines):
        if START_PATTERN.search(line.strip()):
            starts.append(idx + 1)  # 1-based行号
        if END_PATTERN.search(line.strip()):
            ends.append(idx + 1)
    return starts, ends

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    starts, ends = find_structures(lines)
    valid_pairs = []
    for s in starts:
        for e in ends:
            if s < e:
                valid_pairs.append((s, e))
    if valid_pairs:
        return True, valid_pairs
    elif starts or ends:
        return False, 'invalid_order'
    else:
        return False, 'no_components'

def parse_selection(choice, total):
    choice = choice.strip().upper()
    if not choice or choice == 'ALL':
        return list(range(total))
    if choice == 'NO':
        return []
    
    selected = set()
    parts = choice.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start_end = part.split('-', 1)
            try:
                start = int(start_end[0])-1
                end = int(start_end[1])-1
                selected.update(range(start, end+1))
            except:
                continue
        else:
            try:
                num = int(part)-1
                if 0 <= num < total:
                    selected.add(num)
            except:
                continue
    return sorted(selected)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    starts, ends = find_structures(lines)
    valid_structures = []
    for s in starts:
        for e in ends:
            if s < e:
                valid_structures.append((s-1, e-1))  # 转换为0-based
    
    all_invalid = []
    modified_lines = lines.copy()
    
    for s_idx, e_idx in valid_structures:
        start = s_idx + 1
        end = e_idx
        section = modified_lines[start:end]
        invalid = []
        new_section = []
        
        for i, line in enumerate(section, start=start+1):
            stripped = line.strip()
            if stripped.startswith('|') or stripped in (']]', ''):
                new_section.append(line)
                continue
            
            match = PROJECT_LINE_PATTERN.match(line)
            if not match:
                invalid.append((i, line))
                new_section.append(line)
                continue
            
            stars_before, pname, stars_after, rest = match.groups()
            pname_lower = pname.strip().lower()
            translated = REPLACEMENT_RULES.get(pname_lower)
            
            if translated is None:
                print(f"未知项目名 '{pname}' 在文件 {filepath} 行 {i}")
                new_section.append(line)
                continue
            
            new_line = f'> {stars_before}{translated}{stars_after}：{rest}'
            new_section.append(new_line)
        
        if invalid:
            print(f"\n文件 {filepath} 中不符合格式的行：")
            for ln, content in invalid:
                print(f"行 {ln}: {content}")
        
        modified_lines[start:end] = new_section
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified_lines))

def main():
    # 检测文件
    valid_files = []
    invalid_order_files = []
    
    for fname in os.listdir('.'):
        if not (fname.endswith('.ftml') or fname.endswith('.wikidot')):
            continue
        is_valid, reason = check_file(fname)
        if is_valid:
            valid_files.append(fname)
        elif reason == 'invalid_order':
            invalid_order_files.append(fname)
    
    print("\n符合要求的文件：")
    for i, f in enumerate(valid_files, 1):
        print(f"{i}. {f}")
    
    print("\n存在include但顺序错误的文件：")
    for f in invalid_order_files:
        print(f"  {f}")
    
    # 用户选择
    total = len(valid_files)
    if total == 0:
        return
    
    choice = input("\n请选择要处理的文件 (格式如 1,3-5，默认ALL)：")
    selected = parse_selection(choice, total)
    if not selected:
        print("没有选择文件。")
        return
    
    to_process = [valid_files[i] for i in selected]
    
    # 处理文件
    for fpath in to_process:
        process_file(fpath)
    
    # 结束提示
    proceed = input("\n处理完成，是否退出？ (Y/n) ").strip().lower()
    if proceed in ('', 'y'):
        print("退出程序。")
    else:
        print("您可以继续其他操作。")

if __name__ == '__main__':
    main()
