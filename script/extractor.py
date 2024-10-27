import re
import json
import uuid

def extract_chinese_from_html(html_content):
    """
    從 HTML 內容中提取中文，並為每段中文生成唯一鍵名。
    :param html_content: str, HTML 原始內容
    :return: dict, 中文字典
    """
    # 正則表達式：匹配標籤中的中文
    chinese_text_pattern = re.compile(r'>([^<>]*[\u4e00-\u9fff]+[^<>]*)<|["\']([^"\']*[\u4e00-\u9fff]+[^"\']*)["\']')
    chinese_texts = chinese_text_pattern.findall(html_content)

    # 建立字典
    chinese_dict = {}
    for match in chinese_texts:
        # 合併兩組中的文本
        chinese_text = match[0] or match[1]
        
        # 使用 UUID 生成唯一鍵
        unique_key = f"string_{uuid.uuid4().hex[:8]}"
        
        # 添加至字典
        chinese_dict[unique_key] = chinese_text.strip()

    return chinese_dict

def save_dict_to_json(chinese_dict, output_filename="chinese_strings.json"):
    """
    將中文字典保存為 JSON 文件。
    :param chinese_dict: dict, 中文字典
    :param output_filename: str, 輸出文件名
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(chinese_dict, f, ensure_ascii=False, indent=4)

def main(html_filepath, output_json="chinese_strings.json"):
    """
    主函數：讀取 HTML 文件，提取中文並保存為 JSON。
    :param html_filepath: str, HTML 文件路徑
    :param output_json: str, 輸出 JSON 文件名稱
    """
    # 讀取 HTML 文件內容
    with open(html_filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 提取中文並生成字典
    chinese_dict = extract_chinese_from_html(html_content)

    # 保存字典至 JSON 文件
    save_dict_to_json(chinese_dict, output_json)
    print(f"已成功提取中文並保存至 {output_json}")

# 用戶可在此處指定 HTML 文件路徑
if __name__ == "__main__":
    html_filepath = "templates/pixel_tch.html"  # 替換為 HTML 文件路徑
    output_json = "chinese_strings.json"   # 替換為輸出 JSON 文件名稱
    main(html_filepath, output_json)
