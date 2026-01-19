import asyncio
import pytest
from httpx import AsyncClient

from examples.fastapi_llm.app import app

@pytest.mark.asyncio
async def test_summarize_endpoint(monkeypatch):
    async def fake_get_wexin_article(query, top_num=5, max_age_days=14):
        return [
            {"title": "Recent 1", "url": "http://example.com/1", "source": "S1", "date": "2025-12-30 12:00:00"},
            {"title": "Recent 2", "url": "http://example.com/2", "source": "S2", "date": "2025-12-29 12:00:00"}
        ]

    # patch the function used by the example app (imported into module)
    monkeypatch.setattr('examples.fastapi_llm.app.get_wexin_article', fake_get_wexin_article)

    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post('/summarize', json={"query": "AI", "top": 2, "max_age_days": 14})
        assert resp.status_code == 200
        data = resp.json()
        assert 'articles' in data and 'count' in data and data['count'] == 2
        assert isinstance(data['articles'], list)
        assert data['articles'][0]['title'] == 'Recent 1'

        # swagger UI docs should be reachable at /docs
        resp_docs = await client.get('/docs')
        assert resp_docs.status_code == 200
