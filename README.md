<div align="center">
    <img alt="vision_agent" height="200px" src="https://hellomiku.com/img/logo.png"> 
      
# Miku Spider
中文 | [**English**](https://github.com/GobinFan/Miku_Spider/blob/main/README_EN.md)

</div>

## 关于MIKU
AI MIKU是一个基于多智能体(Multiagent)技术的创新AI搜索引擎，致力于为用户提供准确、个性化和实时的搜索结果。作为MIKU生态系统的一部分，Miku Spider专注于高效爬取和处理微信公众号文章。了解更多关于MIKU的信息，请访问：[hellomiku.com](https://hellomiku.com)

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

在开发或调试本地代码时，建议使用 editable install（可编辑安装），这样你修改本地代码后无需反复重装：

```bash
# 可选：先卸载已发布的包以避免混淆
pip uninstall -y miku_ai

# 在仓库根目录执行（将本地代码以可编辑方式安装到当前环境）
pip install -e .

# 安装依赖（如果需要）
pip install -r requirements.txt
```

或者临时运行时把仓库加入 `PYTHONPATH`：

```bash
PYTHONPATH=/path/to/Miku_Spider python your_script.py
```

## 使用方法

以下是一个基本的使用示例：

```python
from miku_ai import get_wexin_article
import asyncio

async def main():
    query = "AI搜索MIKU"
    # fetch top 5 articles within the last 14 days (default)
    articles = await get_wexin_article(query, top_num=5, max_age_days=14)

    # or fetch articles from the last 7 days
    # articles = await get_wexin_article(query, top_num=5, max_age_days=7)

    for article in articles:
        print("标题：", article['title'])
        print("URL：", article['url'])
        print("来源：", article['source'])
        print("日期：", article['date'])
        print("-" * 50)

asyncio.run(main())
```
 
<img alt="MIKU" height="450px" src="https://github.com/user-attachments/assets/4aa6339d-4873-4c15-a7d4-81aa2ff92b14"> 
 

 

## API

### `get_wexin_article(query, top_num=5, max_age_days=14)`

- `query`: 搜索关键词（字符串）
- `top_num`: 返回的最大结果数量（整数，默认为5）
- `max_age_days`: 只返回最近 `max_age_days` 天内发布的文章（整数，默认14）；设为 `None` 则不按时间过滤

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

---

⚠️ 示例项目说明（重要）

仓库中的 `examples/fastapi_llm` 示例已经演化为一个独立项目，名为 **wespider_api**（该项目的初始代码已在仓库内 `wespider_api/` 文件夹中准备好，并已在本地初始化为单独仓库）。

请注意：**wespider_api 依赖于本仓库的部分最新改动（例如 `get_wexin_article` 的可配置 `max_age_days` 参数）**。相关更改已向 upstream（原 miku_ai 仓库）提交了一个 Pull Request；在该 PR 合并并发布新版本到 PyPI 之后，`wespider_api` 将能作为独立项目被正常使用并安装（通过 pip）。

如果你希望我将 `wespider_api` 推到你的 GitHub 并创建对应远程仓库/PR，我可以帮你完成。请在合并 PR 之后再将 `wespider_api` 发布到 PyPI 或你的组织仓库，以避免依赖冲突。

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

From MIKU Team
