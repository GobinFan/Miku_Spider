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

## Usage
Here's a basic usage example:
```python
from miku_ai import get_wexin_article
import asyncio

async def main():
    query = "AI search MIKU"
    articles = await get_wexin_article(query)
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
### `get_wexin_article(query, top_num=5)`
- `query`: Search keyword (string)
- `top_num`: Maximum number of results to return (integer, default is 5)

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

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

From MIKU Team
