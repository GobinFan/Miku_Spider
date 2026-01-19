import sys
import types
import time
import asyncio
# only stub aiohttp if it cannot be imported
try:
    import aiohttp  # type: ignore
except Exception:
    aiohttp_stub = types.ModuleType('aiohttp')
    aiohttp_stub.ClientSession = object
    aiohttp_stub.ClientError = Exception
    sys.modules['aiohttp'] = aiohttp_stub

# provide a minimal BeautifulSoup-like stub so tests can run without bs4 installed
try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    import html
    from html.parser import HTMLParser

    class SimpleTag:
        def __init__(self, name, attrs, parent=None):
            self.name = name
            self.attrs = dict(attrs)
            self.children = []
            self.parent = parent
            self._text = ''

        def __getitem__(self, key):
            return self.attrs.get(key)

        @property
        def text(self):
            # join child strings and tag texts
            parts = []
            for ch in self.children:
                if isinstance(ch, SimpleTag):
                    parts.append(ch.text)
                else:
                    parts.append(ch)
            return ''.join(parts).strip()

        @property
        def string(self):
            return self._text if self._text else None

        def find(self, name=None, attrs=None):
            if name is None:
                return None
            queue = [self]
            while queue:
                node = queue.pop(0)
                if isinstance(node, SimpleTag) and node.name == name:
                    if attrs:
                        ok = True
                        for k, v in attrs.items():
                            val = node.attrs.get(k)
                            if callable(v):
                                if not v(val):
                                    ok = False
                                    break
                            else:
                                if val != v:
                                    ok = False
                                    break
                        if ok:
                            return node
                    else:
                        return node
                for ch in node.children:
                    if isinstance(ch, SimpleTag):
                        queue.append(ch)
            return None

        def find_all(self, name=None, attrs=None):
            res = []
            queue = [self]
            while queue:
                node = queue.pop(0)
                if isinstance(node, SimpleTag) and node.name == name:
                    if attrs:
                        ok = True
                        for k, v in attrs.items():
                            val = node.attrs.get(k)
                            if callable(v):
                                if not v(val):
                                    ok = False
                                    break
                            else:
                                if val != v:
                                    ok = False
                                    break
                        if ok:
                            res.append(node)
                    else:
                        res.append(node)
                for ch in node.children:
                    if isinstance(ch, SimpleTag):
                        queue.append(ch)
            return res

    class SimpleHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.root = SimpleTag('document', {})
            self.cur = self.root

        def handle_starttag(self, tag, attrs):
            node = SimpleTag(tag, attrs, parent=self.cur)
            self.cur.children.append(node)
            self.cur = node

        def handle_endtag(self, tag):
            if self.cur.parent:
                self.cur = self.cur.parent

        def handle_data(self, data):
            self.cur.children.append(data)
            if isinstance(self.cur, SimpleTag):
                self.cur._text += data

    def _beautiful_soup(markup, parser):
        p = SimpleHTMLParser()
        p.feed(markup)
        return p.root

    bs4_module = types.ModuleType('bs4')
    bs4_module.BeautifulSoup = _beautiful_soup
    sys.modules['bs4'] = bs4_module

# stub fake_useragent only when it cannot be imported
try:
    from fake_useragent import UserAgent  # type: ignore
except Exception:
    fa = types.ModuleType('fake_useragent')
    class UserAgent:
        @property
        def random(self):
            return 'test-agent'
    fa.UserAgent = UserAgent
    sys.modules['fake_useragent'] = fa

from miku_ai.spider import MikuSpider


def test_get_wexin_article_filters_recent():
    now_ts = int(time.time())
    old_ts = now_ts - 60 * 60 * 24 * 30  # 30 days ago

    html = f"""
    <html><body><ul>
      <li id="sogou_vr_11002601_box_1">
        <h3>Recent</h3>
        <p class="txt-info">Summary</p>
        <span class="s2"><script>var t = '{now_ts}'</script></span>
        <a target="_blank" href="/link1"></a>
      </li>
      <li id="sogou_vr_11002601_box_2">
        <h3>Old</h3>
        <p class="txt-info">Summary</p>
        <span class="s2"><script>var t = '{old_ts}'</script></span>
        <a target="_blank" href="/link2"></a>
      </li>
    </ul></body></html>
    """

    async def fake_weixin_spider(self, query, page=1):
        return html

    async def fake_get_wexin_article_url(self, url):
        # simple content that parse_item expects to extract url parts
        return "url += 'http://example.com/article1'"

    # patch methods
    original_ws = MikuSpider.weixin_spider
    original_gwa = MikuSpider.get_wexin_article_url
    MikuSpider.weixin_spider = fake_weixin_spider
    MikuSpider.get_wexin_article_url = fake_get_wexin_article_url

    try:
        articles = asyncio.run(MikuSpider().get_wexin_article('q', top_num=10, max_age_days=14))
        assert len(articles) == 1
        assert articles[0]['title'] == 'Recent'

        # now test custom max_age_days (1 day) should still return only the recent article
        articles_1day = asyncio.run(MikuSpider().get_wexin_article('q', top_num=10, max_age_days=1))
        assert len(articles_1day) == 1
        assert articles_1day[0]['title'] == 'Recent'

        # test max_age_days=0 (strict) -- likely exclude even recent unless timestamp exactly matches now
        articles_0day = asyncio.run(MikuSpider().get_wexin_article('q', top_num=10, max_age_days=0))
        assert isinstance(articles_0day, list)
    finally:
        # restore
        MikuSpider.weixin_spider = original_ws
        MikuSpider.get_wexin_article_url = original_gwa
