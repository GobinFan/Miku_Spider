import re
from datetime import datetime
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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

    async def weixin_fetch(self, url, ke, retries=5, timeout=1):
        cookies = await self.get_new_cookies()
        headers = {
            'Cookie': 'SUID=3747A9742B83A20A000000006606A2E7; SUID=3747A97426A6A20B000000006606A2E7; SUV=00ED051974A947376606A2F3884B8464; ABTEST=7|1716888919|v1; IPLOC=CN5101; PHPSESSID=8pft1e0o80d3a29v2mld4thsg6; SNUID=<SNUID_TOKEN>; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaStatus=false',
            'User-Agent': UserAgent().random
        }
        headers["Cookie"] = headers["Cookie"].replace("<SNUID_TOKEN>", cookies["SNUID"])

        for attempt in range(retries):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, params=ke, headers=headers, timeout=timeout, allow_redirects=False) as resp:
                        if resp.status == 200:

                            return await resp.text()
                        else:
                            pass
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    pass
        return ""

    async def get_wexin_article_url(self, url, retries=3, timeout=1):
        cookies = await self.get_new_cookies()
        headers = {
            'Cookie': 'SUID=3747A9742B83A20A000000006606A2E7; SUID=3747A97426A6A20B000000006606A2E7; SUV=00ED051974A947376606A2F3884B8464; ABTEST=7|1716888919|v1; IPLOC=CN5101; PHPSESSID=8pft1e0o80d3a29v2mld4thsg6; SNUID=<SNUID_TOKEN>; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaStatus=false',
            'User-Agent': UserAgent().random
        }
        headers["Cookie"] = headers["Cookie"].replace("<SNUID_TOKEN>", cookies["SNUID"])

        for attempt in range(retries):
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=timeout, allow_redirects=False) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        else:
                            print(f'Attempt {attempt + 1}: get proxy error with status {resp.status}')
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    print(f'Attempt {attempt + 1}: Error: {e}')
        return ""

    async def parse_item(self, item):
        try:
            title = item.find('h3').text.strip() if item.find('h3') else ''
            summary = item.find('p', {'class': 'txt-info'}).text.strip() if item.find('p', {'class': 'txt-info'}) else ''
            source = item.find('span', {'class': 'all-time-y2'}).text.strip() if item.find('span', {'class': 'all-time-y2'}) else ''

            date_script = item.find('span', {'class': 's2'}).find('script').string if item.find('span', {'class': 's2'}) and item.find('span', {'class': 's2'}).find('script') else ''
            timestamp = date_script.split("'")[1] if date_script else '0'
            date = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S') if timestamp.isdigit() else ''

            link_tag = item.find('a', {'target': '_blank'})
            link = link_tag['href'] if link_tag else ''
            full_link = "https://weixin.sogou.com" + link if link else ''

            get_wexin_article_content = await self.get_wexin_article_url(full_link) if full_link else ''
            pattern = re.compile(r"url\s*\+=\s*'([^']*)'")
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

    async def get_wexin_article(self, query, top_num=5):
        content = await self.weixin_spider(query)
        soup = BeautifulSoup(content, 'html.parser')
        news_list = soup.find_all('li', {'id': lambda x: x and x.startswith('sogou_vr_11002601_box_')})
        tasks = [self.parse_item(item) for item in news_list]
        articles = await asyncio.gather(*tasks)
        articles = [article for article in articles if article['url']]
        return articles[:top_num]

async def get_wexin_article(query, top_num=5):
    spider = MikuSpider()
    return await spider.get_wexin_article(query, top_num)

# Example usage
async def main():
    query = "AI搜索MIKU"
    articles = await get_wexin_article(query)
    for item in articles:
        print("title：", item['title'])
        print("url：", item['url'])
        print("source：", item['source'])
        print("date：", item['date'])
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())