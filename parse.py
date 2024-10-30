from bs4 import BeautifulSoup
from collections import defaultdict

import os
import json


def parse_html_to_outline(soup):
    headers = ["h1", "h2", "h3", "h4"]  # 定义标题层级顺序

    def parse_section(element, header_index=0):
        """递归解析每个标题和其下的内容，按标题层级嵌套。"""
        outline = []
        current_level = headers[header_index]  # 当前处理的标题层级
        while element:
            if element.name == current_level:
                # 当前层级标题下的内容
                section = {
                    'title': element.get_text(strip=True),
                    'content': [],
                    'subsections': []
                }
                # 获取当前标题下的内容直到下一个同级或更高层级标题
                sibling = element.find_next_sibling()
                while sibling and (sibling.name not in headers[:header_index + 1]):
                    # 检查是否有下一级标题
                    if header_index + 1 < len(headers) and sibling.name == headers[header_index + 1]:
                        # 递归解析下一级子标题
                        subsection = parse_section(sibling, header_index + 1)
                        section['subsections'].extend(subsection)
                        # 更新sibling为下一个元素
                        if subsection and subsection[-1]['content']:
                            sibling = subsection[-1]['content'][-1].find_next_sibling()
                        else:
                            sibling = None
                    else:
                        section['content'].append(sibling)
                        sibling = sibling.find_next_sibling()
                outline.append(section)
                element = sibling
            else:
                break
        return outline

    # 从第一个 h1 开始解析文档结构
    return parse_section(soup.find(headers[0]))

output_dir = "parsed_headings"
with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "html.parser")
outline = parse_html_to_outline(soup)


def save_outline_to_filesystem(outline, base_path, level_prefix=""):
    """递归地将目录结构保存到文件系统中，并在文件夹名称中加入标题级别。"""
    for idx, section in enumerate(outline, 1):
        # 为当前标题创建一个目录，前缀加上标题级别，如 'h1_', 'h2_' 等
        title_dir = os.path.join(base_path, f"{level_prefix}{idx}_{''.join(filter(lambda x: x.isalnum() or '\u4e00' <= x <= '\u9fff', section['title']))}")
        os.makedirs(title_dir, exist_ok=True)
        
        # 保存当前标题的内容到文件
        content_file_path = os.path.join(title_dir, "content.html")
        with open(content_file_path, "w", encoding="utf-8") as f:
            for content in section['content']:
                f.write(str(content))
        
        # 递归地保存子标题内容，层级前缀递增
        next_level_prefix = f"{level_prefix}{idx}."
        if section['subsections']:
            save_outline_to_filesystem(section['subsections'], title_dir, next_level_prefix)

# 保存到文件系统中的基路径
base_directory = "./docs"
os.makedirs(base_directory, exist_ok=True)

# 调用函数将结构保存到文件系统
save_outline_to_filesystem(outline, base_directory)
print(f"Outline saved to {base_directory}")