 <div align="center">
    <img alt="vision_agent" height="200px" src="https://hellomiku.com/img/logo.png"> 
      
# Miku Spider
English | [**中文**](https://github.com/GobinFan/Miku_Spider/blob/main/README.md)

</div>

## About MIKU
AI MIKU is an innovative AI search engine based on Multiagent technology, dedicated to providing users with accurate, personalized, and real-time search results. As part of the MIKU ecosystem, Miku Spider focuses on efficiently crawling and processing WeChat public account articles. To learn more about MIKU, please visit: [hellomiku.com](https://hellomiku.com)

## Miku Spider Introduction
Miku Spider is a Python tool for searching and retrieving articles from WeChat public accounts. It uses asynchronous methods to improve efficiency and can quickly obtain relevant article information for specified keywords.

## Features
- Asynchronous search of WeChat public account articles
- Retrieval of article title, URL, source, and publication date
- Customizable number of search results
- Use of proxies and User-Agent rotation to avoid bans

## Installation
Install Miku Spider using pip:
```
pip install miku_ai
```

For local development, use an editable install so changes in your working tree take effect immediately:

```bash
# optionally uninstall the released package to avoid confusion
pip uninstall -y miku_ai

# from the repository root
pip install -e .

# install dependencies
pip install -r requirements.txt
```

Or temporarily prioritize the local repo with PYTHONPATH:

```bash
PYTHONPATH=/path/to/Miku_Spider python your_script.py
```

## Usage
Here's a basic usage example:
```python
from miku_ai import get_wexin_article
import asyncio

async def main():
    query = "AI search MIKU"
    # fetch top 5 articles within the last 14 days (default)
    articles = await get_wexin_article(query, top_num=5, max_age_days=14)

    for article in articles:
        print("Title:", article['title'])
        print("URL:", article['url'])
        print("Source:", article['source'])
        print("Date:", article['date'])
        print("-" * 50)

asyncio.run(main())
```

<img alt="MIKU" height="450px" src="https://github.com/user-attachments/assets/4aa6339d-4873-4c15-a7d4-81aa2ff92b14"> 

## API
### `get_wexin_article(query, top_num=5, max_age_days=14)`
- `query`: Search keyword (string)
- `top_num`: Maximum number of results to return (integer, default is 5)
- `max_age_days`: Only include articles published within the last `max_age_days` days (integer, default 14). Use `None` to disable time filtering.

Returns a list of dictionaries, each representing an article, containing the following keys:
- `title`: Article title
- `url`: Article URL
- `source`: Article source (public account name)
- `date`: Publication date
- `snippet`: Article summary

## Notes
- This tool is for learning and research purposes only. Do not use for commercial purposes or large-scale crawling.
- Please comply with the terms of use and regulations of relevant websites when using this tool.
- Excessive use may result in IP bans. Use with caution.

## Contribution
Issues and pull requests are welcome to help improve this project.

---

⚠️ Example project note (important)

The example in this repository `examples/fastapi_llm` has been evolved into a separate project named **wespider_api** (initial code is prepared in the `wespider_api/` folder and initialized as a separate local repository).

Please note: **wespider_api depends on some recent changes to this repository (for example, the configurable `max_age_days` parameter for `get_wexin_article`).** Those changes have been submitted as a Pull Request to the upstream `miku_ai` repository; after the PR is merged and a new version is released on PyPI, `wespider_api` can be published and installed as an independent project.

If you want, I can help push `wespider_api` to your GitHub and create the remote repository / PR; please publish `wespider_api` after the upstream PR merges to avoid dependency mismatches.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

From MIKU Team
