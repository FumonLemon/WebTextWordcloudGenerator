# 网页文本爬取与词云生成工具

这是一个简单的 Python 脚本，用于从指定的网页链接爬取文本内容，进行中文分词、词频统计，并生成词云图片。

## 功能特点

*   支持从多个 URL 爬取文本。
*   将爬取到的文本保存到本地文件。
*   使用 `jieba` 进行中文分词。
*   支持加载停用词文件进行过滤。
*   可以设置词语的最低出现频率和最小长度进行过滤。
*   使用 `wordcloud` 库生成词云图片，支持中文字体。
*   模块化设计 (`scraper.py`, `wordcloud_generator.py`, `main.py`)。

## 安装与使用

1.  **克隆仓库:**
    ```bash
    git clone https://github.com/FumonLemon/WebTextWordcloudGenerator.git
    cd 仓库名
    ```

2.  **创建并激活虚拟环境 (推荐):**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **安装依赖:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置项目:**
    *   编辑 `main.py` 文件。
    *   修改 `target_urls` 列表为你想要爬取的网页链接。
    *   修改 `font_file_path` 为你系统中支持中文的 `.ttf` 字体文件路径。
    *   (可选) 准备 `stop_words.txt` 文件，每行一个停用词。

5.  **运行程序:**
    ```bash
    python main.py
    ```

## 文件说明

*   `main.py`: 程序入口，协调调用爬虫和词云生成模块。
*   `scraper.py`: 负责从网页爬取文本并保存。
*   `wordcloud_generator.py`: 负责文本处理（分词、统计、过滤）和词云生成。
*   `requirements.txt`: 项目依赖的 Python 库列表。
*   `LICENSE`: 项目使用的开源许可证 (MIT)。
*   `README.md`: 项目说明文件。
*   `stop_words.txt` (可选): 用户自定义的停用词列表。
*   `Deng.ttf` (可选): 中文字体文件示例 。

## 注意事项

*   网页结构差异很大，`scraper.py` 中的文本提取方法可能需要根据具体网站进行调整，以获取最相关的正文内容。
*   爬取网站时请遵守网站的 `robots.txt` 协议，并注意不要对服务器造成过大负担。

## 贡献

欢迎对本项目提出改进意见或提交代码贡献！

## 许可证

本项目采用 MIT 许可证。详见 `LICENSE` 文件。
