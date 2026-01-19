import os
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from miku_ai import get_wexin_article

app = FastAPI(title="MIKU Weixin -> LLM Example")

class QueryReq(BaseModel):
    query: str
    top: int = 5
    max_age_days: Optional[int] = 14

async def _call_llm_mock(prompt: str) -> str:
    # Simple mock LLM — replace with real LLM integration
    lines = [l for l in prompt.splitlines() if l.strip()]
    return "MOCK_SUMMARY: " + (lines[0] if lines else "(no content)")

async def _call_llm(prompt: str) -> str:
    # If OPENAI_API_KEY present you can implement an actual call here.
    # For a simple example we return mock summary so the example runs without API keys.
    if os.getenv("OPENAI_API_KEY"):
        # Example placeholder: call OpenAI (user should implement safely, handle errors)
        # import httpx
        # async with httpx.AsyncClient(timeout=10) as client:
        #     resp = await client.post("https://api.openai.com/v1/chat/completions", json={...}, headers={...})
        #     return resp.json()["choices"][0]["message"]["content"].strip()
        return await _call_llm_mock(prompt)
    else:
        return await _call_llm_mock(prompt)

@app.post("/summarize")
async def summarize(req: QueryReq):
    """Fetch articles and return the raw results as JSON.

    Returns:
        {"count": int, "articles": [dict, ...]}
    """
    try:
        articles = await get_wexin_article(req.query, top_num=req.top, max_age_days=req.max_age_days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {e}")

    return {"count": len(articles), "articles": articles}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("examples.fastapi_llm.app:app", host="127.0.0.1", port=8000, reload=True)
