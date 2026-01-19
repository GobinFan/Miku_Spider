import re
from datetime import datetime, timedelta
import aiohttp
import asyncio
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# fallback static User-Agent list to avoid relying on networked fake_useragent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"
]

class MikuSpider:
    def __init__(self):
        self.base_url = 'https://weixin.sogou.com/weixin'

    async def get_new_cookies(self):
        url = 'https://v.sogou.com/v?ie=utf8&query=&p=40030600'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=False) as response:
                cookies = response.cookies
                cookies_dict = {key: morsel.value for key, morsel in cookies.items()}
                return cookies_dict

    async def weixin_fetch(self, url, ke, retries=3, timeout=10):
        cookies = await self.get_new_cookies()
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://weixin.sogou.com/'
        }

        for attempt in range(retries):
            # use session-level cookies from get_new_cookies() to avoid sending stale/static cookie string
            async with aiohttp.ClientSession(cookies=cookies) as session:
                try:
                    async with session.get(url, params=ke, headers=headers, timeout=timeout, allow_redirects=True) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        else:
                            # print(f'Attempt {attempt + 1}: status {resp.status}')
                            pass
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    # print(f'Attempt {attempt + 1}: Error: {e}')
                    pass
            try:
                await asyncio.sleep(1 + attempt)
            except Exception:
                pass
        return ""

    async def get_wexin_article_url(self, url, retries=3, timeout=10):
        cookies = await self.get_new_cookies()
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': 'https://weixin.sogou.com/'
        }

        for attempt in range(retries):
            async with aiohttp.ClientSession(cookies=cookies) as session:
                try:
                    async with session.get(url, headers=headers, timeout=timeout, allow_redirects=True) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        else:
                            print(f'Attempt {attempt + 1}: get proxy error with status {resp.status}')
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    print(f'Attempt {attempt + 1}: Error: {e}')
            try:
                await asyncio.sleep(1 + attempt)
            except Exception:
                pass
        return ""

    async def parse_item(self, item):
        try:
            title = item.find('h3').text.strip() if item.find('h3') else ''
            summary = item.find('p', {'class': 'txt-info'}).text.strip() if item.find('p', {'class': 'txt-info'}) else ''
            source = item.find('span', {'class': 'all-time-y2'}).text.strip() if item.find('span', {'class': 'all-time-y2'}) else ''

            # extract timestamp from <span class="s2"><script>...'</script></span>
            date_script = ''
            span_s2 = item.find('span', {'class': 's2'})
            if span_s2:
                script_tag = span_s2.find('script')
                if script_tag and script_tag.string:
                    date_script = script_tag.string
            date = ''
            try:
                m = re.search(r"['\"](\d{10,13})['\"]", date_script) if date_script else None
                if m:
                    ts = int(m.group(1))
                    if len(m.group(1)) == 13:
                        ts = ts // 1000
                    date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                date = ''

            link_tag = item.find('a', {'target': '_blank'})
            link = link_tag['href'] if link_tag else ''
            full_link = "https://weixin.sogou.com" + link if link else ''

            get_wexin_article_content = await self.get_wexin_article_url(full_link) if full_link else ''
            # accept single- or double-quoted parts when reconstructing the content URL
            pattern = re.compile(r"url\s*\+=\s*['\"]([^'\"]*)['\"]")
            url_parts = pattern.findall(get_wexin_article_content) if get_wexin_article_content else []
            url = ''.join(url_parts).replace('@', '') if url_parts else ''

            return {
                'title': title,
                'snippet': summary,
                'url': url.replace("src=11×tamp", "src=11&timestamp"),
                'source': source,
                'date': date
            }
        except Exception as e:
            print(f"Error parsing item: {e}")
            return {
                'title': '',
                'snippet': '',
                'url': '',
                'source': '',
                'date': ''
            }

    async def weixin_spider(self, query, page=1):
        ke = {'query': f'{query}', 'type': '2', 'page': f'{page}'}
        content = await self.weixin_fetch(self.base_url, ke)
        return content

    async def get_wexin_article(self, query, top_num=5, max_age_days=14):
        """
        Fetch articles for `query`, returning at most `top_num` articles.
        If `max_age_days` is not None, only include articles whose `date`
        is within the last `max_age_days` days.
        """
        content = await self.weixin_spider(query)
        soup = BeautifulSoup(content, 'html.parser')
        # match various sogou result list item id patterns to be more robust
        news_list = soup.find_all('li', id=re.compile(r'^sogou_vr_\d+_box_'))
        tasks = [self.parse_item(item) for item in news_list]
        articles = await asyncio.gather(*tasks)
        articles = [article for article in articles if article['url']]

        if max_age_days is not None:
            cutoff = datetime.now() - timedelta(days=max_age_days)
            recent = []
            for article in articles:
                try:
                    article_date = datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                    if article_date >= cutoff:
                        recent.append(article)
                except Exception:
                    # skip items with invalid/empty date
                    continue
            articles = recent

        return articles[:top_num]

async def get_wexin_article(query, top_num=5, max_age_days=14):
    spider = MikuSpider()
    return await spider.get_wexin_article(query, top_num, max_age_days)

# Example usage: prints results as JSON. When run as a script, you can pass arguments:
#   python -m miku_ai.spider --query "AI搜索MIKU" --top 5 --max-age 14
# Use --max-age -1 to disable time filtering.
async def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Fetch Weixin articles and output JSON')
    parser.add_argument('--query', '-q', default='AI搜索MIKU', help='search query')
    parser.add_argument('--top', '-n', type=int, default=5, help='maximum number of articles to return')
    parser.add_argument('--max-age', '-m', type=int, default=14, help='maximum age in days (use -1 to disable)')
    args = parser.parse_args()

    max_age = None if args.max_age is None or args.max_age < 0 else args.max_age

    articles = await get_wexin_article(args.query, top_num=args.top, max_age_days=max_age)

    # print JSON to stdout
    print(json.dumps(articles, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())