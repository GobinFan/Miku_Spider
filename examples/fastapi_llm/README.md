# Example: FastAPI + LLM integration (using local miku_ai)

This example shows how to use `miku_ai.get_wexin_article` in a small FastAPI app that calls an LLM (mock by default).

Quick start (development):

1. Install package in editable mode from repo root (so local changes are used):

```bash
# from repo root
pip install -e .
```

2. Create and activate a virtualenv or conda env, then install example deps:

```bash
pip install -r examples/fastapi_llm/requirements.txt
```

3. Run the example app:

```bash
uvicorn examples.fastapi_llm.app:app --reload --port 7000
```

4. Test the endpoint:

```bash
curl -X POST "http://localhost:7000/summarize" -H "Content-Type: application/json" -d '{"query":"AI搜索MIKU","top":2,"max_age_days":14}'
```

Swagger UI / OpenAPI docs:

- FastAPI exposes an interactive Swagger UI at `http://localhost:7000/docs` and ReDoc at `http://localhost:7000/redoc`.
- After starting the server (see below), open your browser to `http://localhost:7000/docs` to interactively test the `/summarize` endpoint.

Run the server (two options):

- Using uvicorn directly:

```bash
uvicorn examples.fastapi_llm.app:app --reload --host 127.0.0.1 --port 7000
```

- Or use the convenience script:

```bash
chmod +x examples/fastapi_llm/run.sh
./examples/fastapi_llm/run.sh 127.0.0.1 7000
```

Notes:
- The example returns raw article JSON from the `/summarize` endpoint and does not perform any LLM calls by default. You can extend the example to call an LLM (e.g., in `_call_llm`) if needed.
- This example is minimal — for production consider proper timeouts, retries, authentication, and rate-limiting.
