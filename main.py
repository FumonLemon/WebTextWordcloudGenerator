import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import re # 用于简单的文本清理

# --- 配置 ---
input_file_path = 'input_text.txt'  # <-- 将你的文本内容粘贴到这个文件中
output_wordcloud_file = 'simple_wordcloud.png' # 输出的词云图片文件名
font_file_path = r'C:\Users\Lenovo\Desktop\魔法工具与作品\python\词云\Deng.ttf'
# <-- 替换为你系统中的中文ttf字体文件路径
# 停用词文件 (可选)，每行一个停用词
# 可以自己创建一个 stop_words.txt 文件，或者使用网上现成的
stopwords_file_path = 'stop_words.txt' # <-- 停用词文件路径 (如果不存在会跳过)

# --- 1. 读取文本文件 ---
def read_text_file(filepath):
    text = ""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"成功读取文件: {filepath}")
    except FileNotFoundError:
        print(f"错误：文件未找到 - {filepath}")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
    return text

# --- 2. 文本清理 (简化版) ---
def clean_simple_text(text):
    # 移除标点符号和特殊字符，只保留中文、英文和数字
    # 根据需要调整正则表达式
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '', text)
    return cleaned_text

# --- 3. 中文分词 ---
def segment_text(text):
    # 使用jieba进行分词，返回生成器
    return jieba.cut(text, cut_all=False)

# --- 4. 加载停用词 (可选) ---
def load_stopwords(filepath):
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

# --- 5. 词频统计和过滤 ---
def count_and_filter_words(word_generator, stop_words, min_freq=1, min_len=1):
    word_counts = Counter()
    for word in word_generator:
        word = word.strip().lower() # 去除首尾空格并转小写
        if word and word not in stop_words and len(word) >= min_len:
             word_counts[word] += 1

    # 过滤低频词
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_freq}

    print(f"分词及过滤后，剩余 {len(filtered_word_counts)} 个词语用于词云生成。")
    # print("出现频率最高的20个词:", Counter(filtered_word_counts).most_common(20)) # 可以打印出来看看
    return filtered_word_counts

# --- 6. 生成词云 ---
def generate_wordcloud(word_counts, output_filename, font_path):
    if not word_counts:
        print("错误：没有词语可以生成词云。")
        return

    if not font_path or not os.path.exists(font_path):
        print(f"错误：未找到有效的字体文件 - {font_path}")
        print("请确保 font_file_path 指向一个支持中文的 .ttf 字体文件。")
        return

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
        return

    # 保存图片
    try:
        wc.to_file(output_filename)
        print(f"词云已保存到 {output_filename}")
         # 也可以使用matplotlib显示图片 (可选)
        # plt.figure(figsize=(10, 8))
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off") # 不显示坐标轴
        # plt.show()
    except Exception as e:
        print(f"保存词云图片时发生错误: {e}")


# --- 主程序 ---
if __name__ == "__main__":
    # 1. 准备输入文件 (手动创建并粘贴内容)
    # 请确保 input_text.txt 文件存在，并将你想分析的文本内容粘贴进去

    # 2. 读取文本
    raw_text = read_text_file(input_file_path)

    if raw_text:
        # 3. 清理文本
        print("正在清理文本...")
        cleaned_text = clean_simple_text(raw_text)

        # 4. 中文分词
        print("正在进行中文分词...")
        word_generator = segment_text(cleaned_text)

        # 5. 加载停用词 (可选)
        stop_words = load_stopwords(stopwords_file_path)

        # 6. 词频统计和过滤
        print("正在统计词频并过滤...")
        # 可以根据需要调整 min_freq (最小词频) 和 min_len (最小词长)
        filtered_word_counts = count_and_filter_words(
            word_generator,
            stop_words,
            min_freq=3, # 词语至少出现3次
            min_len=2   # 词语长度至少为2
        )

        # 7. 生成词云
        print("正在生成词云图片...")
        generate_wordcloud(
            filtered_word_counts,
            output_wordcloud_file,
            font_file_path
        )

        print("程序执行完毕。")
    else:
        print("没有文本内容可供处理。请检查 input_text.txt 文件。")

