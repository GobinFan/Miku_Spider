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
