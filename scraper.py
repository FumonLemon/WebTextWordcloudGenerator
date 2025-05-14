# scraper.py
import requests
from bs4 import BeautifulSoup
import os
import re

def scrape_and_save_text(urls, output_filepath):
    """
    从给定的URL列表中爬取网页文本，并保存到指定文件。

    Args:
        urls (list): 包含要爬取的网页链接的列表。
        output_filepath (str): 爬取到的文本要保存到的文件路径。

    Returns:
        bool: 如果成功爬取并保存了至少一部分文本，返回True；否则返回False。
    """
    all_text = ""
    print(f"--- 开始爬取 {len(urls)} 个网页 ---")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } # 模拟浏览器访问

    for i, url in enumerate(urls):
        print(f"正在爬取 ({i+1}/{len(urls)}): {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15) # 增加超时时间
            response.raise_for_status() # 检查HTTP请求是否成功

            # 设置编码，优先使用响应头中的编码，否则使用utf-8
            response.encoding = response.apparent_encoding if response.apparent_encoding else 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # --- 提取文本的核心部分 ---
            # 简单的提取所有可见文本，可能包含导航、广告等非正文内容
            # 对于更精确的正文提取，需要分析具体网站的HTML结构
            # 比如可以尝试查找 <article>, <main>, <div class="content"> 等标签
            text = soup.get_text()

            # 简单的文本清理：移除多余的空白行和空格
            text = os.linesep.join([s for s in text.splitlines() if s.strip()]) # 移除空行
            text = re.sub(r'\s+', ' ', text).strip() # 将多个连续空白符替换为单个空格

            if text: # 只添加非空文本
                all_text += f"--- Start of Content from {url} ---\n"
                all_text += text
                all_text += f"\n--- End of Content from {url} ---\n\n"
                print(f"成功爬取并提取文本: {url}")
            else:
                 print(f"警告: 从 {url} 未提取到有效文本。")


        except requests.exceptions.Timeout:
             print(f"爬取网页时发生超时错误 {url}")
        except requests.exceptions.RequestException as e:
            print(f"爬取网页时发生错误 {url}: {e}")
        except Exception as e:
            print(f"处理网页内容时发生错误 {url}: {e}")

    # 保存所有爬取到的文本到一个文件
    if all_text.strip(): # 如果有内容才保存
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(all_text)
            print(f"--- 所有爬取到的文本已保存到 {output_filepath} ---")
            return True # 表示成功保存
        except Exception as e:
            print(f"保存爬取文本到文件时发生错误: {e}")
            return False
    else:
        print("--- 没有爬取到有效文本内容 ---")
        return False

# 如果直接运行这个文件，可以用于测试爬虫功能
if __name__ == "__main__":
    test_urls = [
        'https://news.sina.com.cn/',
        'https://www.baidu.com/', # 百度首页可能文本杂乱
        'https://example.com/'
    ]
    test_output_file = 'test_scraped.txt'
    scrape_and_save_text(test_urls, test_output_file)
    print(f"测试完成。请检查文件 {test_output_file}")
