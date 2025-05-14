# main.py
from scraper import scrape_and_save_text
from wordcloud_generator import (
    read_text_file,
    clean_text,
    segment_text,
    load_stopwords,
    count_and_filter_words,
    generate_wordcloud_image
)
import os

# --- 主要配置 ---
# 要爬取的网页URL列表
target_urls = [
    'https://www.lemonfumo.top/index.php/archives/185', # 示例：博客文章链接
    #'https://www.example.com/'
]

# 爬取到的文本保存文件
scraped_output_file = 'scraped_website_text.txt'

# 词云生成配置
wordcloud_output_file = 'website_wordcloud.png'
# 请将此路径替换为你系统中支持中文的 .ttf 字体文件路径
# 使用原始字符串 r'' 可以避免反斜杠转义问题
font_file_path = r'C:\Users\Lenovo\Desktop\魔法工具与作品\python\词云\Deng.ttf'

# 停用词文件 (可选)
stopwords_file_path = 'stop_words.txt' # 确保文件存在或忽略此行

# 词频统计和过滤配置
min_frequency = 3 # 词语至少出现的次数
min_length = 2    # 词语的最小长度

# --- 主流程 ---
if __name__ == "__main__":
    print("--- 启动程序 ---")

    # 1. 调用爬虫模块爬取网页并保存文本
    print("\n--- 执行网页爬取 ---")
    scrape_success = scrape_and_save_text(target_urls, scraped_output_file)

    if scrape_success:
        # 2. 调用词云生成模块处理文本并生成词云
        print("\n--- 执行词云生成 ---")
        raw_text = read_text_file(scraped_output_file)

        if raw_text:
            # 文本清理
            print("正在清理文本...")
            cleaned_text = clean_text(raw_text)

            # 中文分词
            print("正在进行中文分词...")
            word_generator = segment_text(cleaned_text)

            # 加载停用词 (如果文件存在)
            stop_words = load_stopwords(stopwords_file_path)

            # 词频统计和过滤
            print("正在统计词频并过滤...")
            filtered_word_counts = count_and_filter_words(
                word_generator,
                stop_words,
                min_freq=min_frequency,
                min_len=min_length
            )

            # 生成词云
            print("正在生成词云图片...")
            generate_wordcloud_image(
                filtered_word_counts,
                wordcloud_output_file,
                font_file_path
            )
        else:
            print("没有文本内容可供处理（爬取文件可能为空）。")
    else:
        print("网页爬取失败，无法进行后续词云生成。")

    print("\n--- 程序执行完毕 ---")
