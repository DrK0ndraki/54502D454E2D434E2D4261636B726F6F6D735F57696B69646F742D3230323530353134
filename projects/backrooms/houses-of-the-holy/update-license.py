import os
import re
import sys


def find_files_with_license_box():
    """Find .ftml or .wikidot files in the current directory containing the license box."""
    files_with_license = []
    
    for file in os.listdir('.'):
        if file.endswith(('.ftml', '.wikidot')):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "[[include :backrooms-wiki-cn:component:license-box" in content:
                        files_with_license.append(file)
            except Exception as e:
                print(f"Error reading {file}: {e}")
    
    return files_with_license


def parse_user_selection(input_str, max_index):
    """Parse user selection like '1', '3-4', '1,3-5', 'ALL', 'NO'."""
    if not input_str or input_str.upper() == 'ALL':
        return list(range(1, max_index + 1))
    
    if input_str.upper() == 'NO':
        return []
    
    selected = set()
    parts = input_str.split(',')
    
    for part in parts:
        if '-' in part:
            start, end = map(str.strip, part.split('-'))
            try:
                start_num = int(start)
                end_num = int(end)
                if start_num < 1 or end_num > max_index:
                    print(f"Warning: Range {start}-{end} out of bounds. Using valid portion.")
                start_num = max(1, start_num)
                end_num = min(max_index, end_num)
                selected.update(range(start_num, end_num + 1))
            except ValueError:
                print(f"Warning: Invalid range '{part}'. Skipping.")
        else:
            try:
                num = int(part.strip())
                if 1 <= num <= max_index:
                    selected.add(num)
                else:
                    print(f"Warning: Index {num} out of bounds. Skipping.")
            except ValueError:
                print(f"Warning: Invalid input '{part}'. Skipping.")
    
    return sorted(list(selected))


def analyze_license_box(content):
    """Analyze the license box format and extract parameters."""
    # Check for single-line format
    single_line_match = re.search(r'\[\[include :backrooms-wiki-cn:component:license-box\s+(.*?)\]\]', content, re.DOTALL)
    
    # Check for multi-line format
    multi_line_match = re.search(r'\[\[include :backrooms-wiki-cn:component:license-box\s*\n(.*?)\]\]', content, re.DOTALL)
    
    has_single_line = bool(single_line_match)
    has_multi_line = bool(multi_line_match)
    
    if has_single_line and has_multi_line:
        return None, None, None, "mixed"  # Mixed format
    
    if has_single_line:
        # Single-line format
        params_str = single_line_match.group(1).strip()
        params = {}
        if params_str:
            param_matches = re.findall(r'(\w+)=([^\s]+)', params_str)
            for param, value in param_matches:
                params[param] = value
        return params, single_line_match.group(0), None, "single"
    
    if has_multi_line:
        # Multi-line format
        params_block = multi_line_match.group(1)
        params = {}
        for line in params_block.strip().split('\n'):
            line = line.strip()
            if line.startswith('|'):
                param_match = re.match(r'\|(\w+)=(.+?)$', line)
                if param_match:
                    param, value = param_match.groups()
                    params[param] = value.strip()
        return params, None, multi_line_match.group(0), "multi"
    
    return None, None, None, "none"  # No valid format found


def update_license_box(content, old_box, box_format, params):
    """Update the license box with new parameters."""
    if box_format == "single":
        # Create new single-line format
        param_str = " ".join([f"{key}={value}" for key, value in params.items()])
        new_box = f"[[include :backrooms-wiki-cn:component:license-box {param_str}]]"
        return content.replace(old_box, new_box)
    
    elif box_format == "multi":
        # Create new multi-line format
        param_lines = [f"|{key}={value}" for key, value in params.items()]
        new_box = "[[include :backrooms-wiki-cn:component:license-box\n" + "\n".join(param_lines) + "\n]]"
        return content.replace(old_box, new_box)
    
    return content


def main():
    print("License Module Editor for Backrooms Wiki Files")
    print("=" * 50)
    
    # Step 1: Find files with license box
    files_with_license = find_files_with_license_box()
    
    if not files_with_license:
        print("No files containing license box found in the current directory.")
        return
    
    print(f"Found {len(files_with_license)} file(s) with license box:")
    for i, file in enumerate(files_with_license, 1):
        print(f"{i}. {file}")
    
    # Step 2: Ask user which files to edit
    selection_input = input("\nSelect files to edit (e.g., '1', '3-4', '1,3-5', 'ALL', 'NO', default is ALL): ").strip()
    selected_indices = parse_user_selection(selection_input, len(files_with_license))
    
    if not selected_indices:
        print("No files selected for editing. Exiting.")
        return
    
    selected_files = [files_with_license[i-1] for i in selected_indices]
    print(f"\nSelected {len(selected_files)} file(s) for editing.")
    
    # Step 4: Get parameter values from user
    default_lang = "EN"
    
    # Process each selected file
    for file in selected_files:
        print(f"\nProcessing file: {file}")
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Step 3: Analyze license box
            params, single_line_box, multi_line_box, box_format = analyze_license_box(content)
            
            if box_format == "mixed":
                print(f"Warning: File '{file}' contains both single-line and multi-line license box formats. Skipping.")
                continue
            
            if box_format == "none":
                print(f"Warning: Could not identify license box format in '{file}'. Skipping.")
                continue
            
            print(f"Found license box in {box_format}-line format with parameters: {params}")
            
            # Get author parameter
            if 'author' in params:
                author_input = input(f"Enter author(s) separated by '、' (current: {params['author']}, press Enter to keep): ").strip()
                if author_input:
                    params['author'] = author_input
            else:
                author_input = input("Enter author(s) separated by '、' (none defined, press Enter to skip): ").strip()
                if author_input:
                    params['author'] = author_input
            
            # Get lang parameter
            if 'lang' in params:
                lang_input = input(f"Enter language (current: {params['lang']}, default: {default_lang}, press Enter to use default): ").strip()
                params['lang'] = lang_input if lang_input else default_lang
            else:
                lang_input = input(f"Enter language (none defined, default: {default_lang}, press Enter to use default): ").strip()
                params['lang'] = lang_input if lang_input else default_lang
            
            # Get translator parameter
            if 'translator' in params:
                translator_input = input(f"Enter translator(s) separated by '、' (current: {params['translator']}, press Enter to keep): ").strip()
                if translator_input:
                    params['translator'] = translator_input
            else:
                translator_input = input("Enter translator(s) separated by '、' (none defined, press Enter to skip): ").strip()
                if translator_input:
                    params['translator'] = translator_input
            
            # Step 5: Update license box
            old_box = single_line_box if box_format == "single" else multi_line_box
            updated_content = update_license_box(content, old_box, box_format, params)
            
            # Write updated content back to file
            with open(file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Successfully updated license box in '{file}'")
        
        except Exception as e:
            print(f"Error processing file '{file}': {e}")
    
    print("\nLicense module editing completed.")


if __name__ == "__main__":
    main()
