<div align="center">
    <img alt="vision_agent" height="200px" src="https://hellomiku.com/img/logo.png"> 
      
# Miku Spider
</div>

## 关于MIKU
MIKU是一个基于多智能体(Multiagent)技术的创新AI搜索引擎，致力于为用户提供准确、个性化和实时的搜索结果。作为MIKU生态系统的重要组成部分，Miku Spider专注于高效爬取和处理微信公众号文章。了解更多关于MIKU的信息，请访问：[hellomiku.com](https://hellomiku.com)

## Miku Spider 简介
Miku Spider 是一个用于搜索和获取微信公众号文章的 Python 工具。它使用异步方法来提高效率，能够快速获取指定关键词的相关文章信息。

## 特性

- 异步搜索微信公众号文章
- 获取文章标题、URL、来源和发布日期
- 可自定义搜索结果数量
- 使用代理和 User-Agent 轮换以避免被封禁

## 安装

使用 pip 安装 Miku Spider：

```
pip install miku_ai
```

## 使用方法

以下是一个基本的使用示例：

```python
from miku_ai import get_wexin_article
import asyncio

async def main():
    query = "AI搜索MIKU"
    articles = await get_wexin_article(query)
    for article in articles:
        print("标题：", article['title'])
        print("URL：", article['url'])
        print("来源：", article['source'])
        print("日期：", article['date'])
        print("-" * 50)

asyncio.run(main())
```

## API

### `get_wexin_article(query, top_num=5)`

- `query`: 搜索关键词（字符串）
- `top_num`: 返回的最大结果数量（整数，默认为5）

返回一个包含字典的列表，每个字典代表一篇文章，包含以下键：
- `title`: 文章标题
- `url`: 文章URL
- `source`: 文章来源（公众号名称）
- `date`: 发布日期
- `snippet`: 文章摘要

## 注意事项

- 本工具仅用于学习和研究目的，请勿用于商业用途或大规模爬取。
- 使用本工具时请遵守相关网站的使用条款和规定。
- 过度使用可能导致 IP 被封禁，请谨慎使用。

## 贡献

欢迎提交 issues 和 pull requests 来帮助改进这个项目。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。


这个 README 包含了以下几个主要部分：

1. 项目简介
2. 主要特性
3. 安装指南
4. 使用方法和示例代码
5. API 说明
6. 注意事项
7. 贡献指南
8. 许可证信息

你可以根据你的具体需求和项目特点来调整这个 README。一个好的 README 应该能让用户快速了解你的项目是做什么的，如何安装和使用，以及如何贡献到项目中。

记得随着项目的发展不断更新 README，保持信息的及时性和准确性。

From MIKU Team
