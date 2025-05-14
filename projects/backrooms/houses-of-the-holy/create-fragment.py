import argparse
import re

def parse_suffix(suffix_str):
    """解析用户输入的后缀范围"""
    parts = suffix_str.split(',')
    numbers = []
    for part in parts:
        part = part.strip()
        if '-' in part:
            # 处理数字范围 (例如 3-5)
            range_match = re.match(r'^(\d+)-(\d+)$', part)
            if not range_match:
                raise ValueError(f"无效的范围格式: {part}")
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start > end:
                raise ValueError(f"无效的范围: {start} > {end}")
            numbers.extend(range(start, end + 1))
        else:
            # 处理单个数字
            if not part.isdigit():
                raise ValueError(f"无效的数字: {part}")
            numbers.append(int(part))
    return numbers

def create_filename(prefix, name, suffix_num, ext):
    """生成规范化的文件名"""
    filename = []
    if prefix:
        filename.append(f"{prefix}:")  # 添加前缀和冒号
    filename.append(name)              # 主体名称
    if suffix_num is not None:
        filename.append(f"-{suffix_num}")  # 后缀和数字
    filename.append(f".{ext}")         # 扩展名
    return ''.join(filename)

def main():
    # 配置命令行参数解析
    parser = argparse.ArgumentParser(
        description="批量文件创建工具",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-p", "--prefix", 
                       help="可选前缀 (格式：前缀:)")
    parser.add_argument("-n", "--name", required=True,
                       help="必需的文件主体名称")
    parser.add_argument("-s", "--suffix",
                       help="可选后缀范围，支持格式：\n"
                            "1) 单个数字：5\n"
                            "2) 数字范围：1-3\n"
                            "3) 组合格式：1,3-5")
    parser.add_argument("-e", "--ext", required=True,
                       help="必需的文件扩展名 (例如 txt)")

    args = parser.parse_args()

    # 处理后缀参数
    suffix_numbers = []
    if args.suffix:
        try:
            suffix_numbers = parse_suffix(args.suffix)
        except ValueError as e:
            print(f"错误：{e}")
            return

    # 创建主要文件
    if args.suffix:
        # 批量创建模式
        for num in suffix_numbers:
            filename = create_filename(args.prefix, args.name, num, args.ext)
            open(filename, 'w').close()
            print(f"已创建文件：{filename}")
    else:
        # 单个文件模式
        filename = create_filename(args.prefix, args.name, None, args.ext)
        open(filename, 'w').close()
        print(f"已创建文件：{filename}")

    # 特殊处理：当prefix是fragment时
    if args.prefix and args.prefix.lower() == "fragment":
        # 询问用户是否创建基础文件
        while True:
            choice = input("\n是否要创建基础文件 [名称].[扩展名]? (y/n) ").strip().lower()
            if choice in ['y', 'yes']:
                # 生成基础文件名
                base_file = create_filename(None, args.name, None, args.ext)
                open(base_file, 'w').close()
                print(f"已创建基础文件：{base_file}")
                break
            elif choice in ['n', 'no']:
                print("已跳过基础文件创建")
                break
            else:
                print("无效输入，请输入 y/yes 或 n/no")

if __name__ == "__main__":
    main()
