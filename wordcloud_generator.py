# wordcloud_generator.py
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re

# --- 文本处理和词云生成函数 ---

def read_text_file(filepath):
    """读取文本文件内容"""
    text = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"成功读取文件: {filepath}")
    except FileNotFoundError:
        print(f"错误：文件未找到 - {filepath}")
        print("请确保输入文件存在且路径正确。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return text

def clean_text(text):
    """简单的文本清理：移除标点符号和特殊字符，只保留中文、英文和数字"""
    # 可以根据需要调整正则表达式
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '', text)
    return cleaned_text

def segment_text(text):
    """使用jieba进行中文分词"""
    # cut_all=False 表示精确模式
    return jieba.cut(text, cut_all=False)

def load_stopwords(filepath):
    """加载停用词文件"""
    stop_words = set()
    if filepath and os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    stop_words.add(line.strip())
            print(f"成功加载停用词文件: {filepath}")
        except Exception as e:
            print(f"加载停用词文件时发生错误: {e}")
    elif filepath:
         print(f"Warning: 停用词文件未找到: {filepath}. 跳过停用词过滤。")
    return stop_words

def count_and_filter_words(word_generator, stop_words, min_freq=1, min_len=1):
    """统计词频并过滤停用词、低频词和短词"""
    word_counts = Counter()
    for word in word_generator:
        word = word.strip().lower() # 去除首尾空格并转小写
        if word and word not in stop_words and len(word) >= min_len:
             word_counts[word] += 1

    # 过滤低频词
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_freq}

    print(f"分词及过滤后，剩余 {len(filtered_word_counts)} 个词语用于词云生成。")
    # 可以打印出来看看出现频率最高的词
    # print("出现频率最高的20个词:", Counter(filtered_word_counts).most_common(20))
    return filtered_word_counts

def generate_wordcloud_image(word_counts, output_filename, font_path):
    """根据词频字典生成词云图片"""
    if not word_counts:
        print("错误：没有词语可以生成词云。")
        return False

    if not font_path or not os.path.exists(font_path):
        print(f"错误：未找到有效的字体文件 - {font_path}")
        print("请确保 font_path 指向一个支持中文的 .ttf 字体文件。")
        return False

    # 创建WordCloud对象
    wc = WordCloud(
        font_path=font_path,       # 必须指定支持中文的字体
        background_color="white",  # 背景颜色
        max_words=2000,            # 最大显示的词语数量
        width=800,                 # 图片宽度
        height=600,                # 图片高度
        margin=5,                  # 词语之间的距离
        random_state=42,           # 随机状态，保证每次生成的词云形状一样
        collocations=False,        # 是否包括双词搭配，对于中文通常设置为False
    )

    # 从词频字典生成词云
    try:
        wc.generate_from_frequencies(word_counts)
    except Exception as e:
        print(f"生成词云时发生错误: {e}")
        return False

    # 保存图片
    try:
        wc.to_file(output_filename)
        print(f"词云已保存到 {output_filename}")
        return True
         # 也可以使用matplotlib显示图片 (可选)
        # plt.figure(figsize=(10, 8))
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off") # 不显示坐标轴
        # plt.show()
    except Exception as e:
        print(f"保存词云图片时发生错误: {e}")
        return False

# 如果直接运行这个文件，可以用于测试词云生成功能 (需要一个input_text.txt)
if __name__ == "__main__":
    test_input_file = 'test_scraped.txt' # 需要手动创建并填充内容
    test_output_wordcloud = 'test_wordcloud.png'
    test_font_path = r'C:\Windows\Fonts\simhei.ttf' # 替换为你的字体路径
    test_stopwords_path = 'stop_words.txt' # 可选

    text_content = read_text_file(test_input_file)

    if text_content:
        cleaned_text = clean_text(text_content)
        word_generator = segment_text(cleaned_text)
        stop_words = load_stopwords(test_stopwords_path)
        word_counts = count_and_filter_words(word_generator, stop_words, min_freq=2, min_len=2)
        generate_wordcloud_image(word_counts, test_output_wordcloud, test_font_path)
    else:
        print("没有文本内容用于生成测试词云。")
