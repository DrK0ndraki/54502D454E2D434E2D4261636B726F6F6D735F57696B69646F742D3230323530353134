# Documentation

**UNOFFICIAL Translation Project Repository**

> **Note:** This repository is for internal use only and is not intended for public distribution.

## 说明

本仓库专用于翻译项目，主要用于存储翻译文档及相关工具。

仓库名称采用 ASCII 字符串转换为 16 进制代码的形式，以避免通过特定关键词（如 Backrooms、FTML 等）被无关人士发现。

实际名称为 “TP-EN-CN-Backrooms_Wikidot-20250514”，其含义如下：
- **TP**: 翻译项目（Translation Project）。
- **EN**: 英文（English），表示原文语言。
- **CN**: 中文（Chinese），表示译文语言。
- **Backrooms_Wikidot**: 翻译内容的来源网站。
- **20250514**: 翻译日期。

### 目录结构

```
├── plugins
├── projects
│   ├── 网站文件夹
│   │   ├── 项目文件夹
│   │   │   ├── 原文文件夹（EN）
│   │   │   │   ├── 原文代码文件
│   │   │   ├── 译文文件夹（CN）
│   │   │   │   ├── 译文代码文件
│   │   │   └── termbase.ini
│   │   └── DIR_README.MD
├── README.MD
├── LICENSE
``` 

### 目录说明

- **plugins**: 存放用于处理翻译项目的自动化插件，请勿随意使用。
- **projects**: 存放翻译项目。
  - **网站文件夹**: 按原文来源网站分类。本仓库仅存放来自 The Backrooms Wikidot 中文维基的翻译项目。例如：`backrooms` 文件夹存放所有相关翻译内容。
    - **项目文件夹**: 每篇文章单独一个文件夹，例如 `level-1` 对应 Level 1。
      - **原文文件夹（EN）**: 存放原文文本，文件夹名称使用语言代码（即 EN）。
        - **原文代码文件**: 原文代码文件（ftml 格式），文件名与链接一致。例如：`level-1.ftml` 对应 Level 1 的链接 `level-1`。
        - **对于迭代文章**: 文件名使用 fragment 链接名，务必将链接中的冒号（:）替换为下划线（_）。例如：`fragment_defrag-0.ftml`，`fragment_defrag-1.ftml`。
      - **译文文件夹（CN）**: 存放译文文本，文件夹名称使用语言代码（即 CN）。
        - **译文代码文件**: 译文代码文件（ftml 格式），命名规则与原文相同。
        - **对于迭代文章**: 文件名使用 fragment 链接名，链接中的冒号（:）替换为下划线（_）。例如：`fragment_defrag-0.ftml`，`fragment_defrag-1.ftml`。
      - **termbase.ini**: 项目自定义术语库，仅供 AI 修改参考，无其他用途。
    - **DIR_README.MD**: 项目文件夹的说明文档。注意：GitHub 不允许空文件夹，每级目录必须至少包含一个文件。
- **README.MD**: 仓库的说明文档，请勿删除。
- **LICENSE**: 仓库的许可文件，请勿删除。

### 规则

1. 本仓库所有内容均为翻译项目内容，禁止任何形式的转载和使用。
2. 文件名仅允许使用**字母、数字、横线、下划线**，其他字符需替换为**下划线（_）**。
   - 对于迭代文章，文件名使用 fragment 链接名，务必将链接中的冒号（:）替换为下划线（_）。例如：`fragment_defrag-0`，`fragment_defrag-1`。
3. 语言代码（如 EN、CN）必须大写；其他文件夹和文件名必须小写。
4. 请勿直接修改本仓库文件。如需修改，请 fork 后提交 PR。
5. 每级目录**必须至少包含一个文件**，GitHub 不允许空文件夹，请在每级目录下创建一个 DIR_README.MD 或 .gitkeep 文件，内容可以为空。
6. 请勿随意删除或修改 README.MD 和 LICENSE 文件。
7. 本人保留对本仓库内容的最终解释权。