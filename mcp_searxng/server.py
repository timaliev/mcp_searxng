"""MCP server for SearXNG web search."""

import os
import sys
import logging

import httpx
from mcp.server import MCPServer

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("mcp-searxng")

server = MCPServer("searxng", version="0.1.0")

SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:8080/searxng").rstrip("/")
_client: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=30.0)
    return _client


def _search(
    query: str,
    categories: list[str] | None = None,
    engines: list[str] | None = None,
    max_results: int = 10,
    language: str | None = None,
) -> dict:
    """Low-level search against SearXNG JSON API."""
    params = {
        "q": query,
        "format": "json",
        "pageno": 1,
        "language": language or "auto",
    }
    if categories:
        params["categories"] = ",".join(categories)
    if engines:
        params["engines"] = ",".join(engines)

    try:
        resp = _get_client().get(f"{SEARXNG_URL}/search", params=params)
        resp.raise_for_status()
        data = resp.json()
    except httpx.ConnectError:
        return {"success": False, "error": "ECONNREFUSED", "detail": f"Cannot reach SearXNG at {SEARXNG_URL}"}
    except httpx.HTTPStatusError as e:
        return {"success": False, "error": "ESEARCH", "detail": f"SearXNG returned {e.response.status_code}"}
    except Exception as e:
        logger.exception("Search failed")
        return {"success": False, "error": "EPROCESSING", "detail": str(e)}

    results = []
    for r in data.get("results", [])[:max_results]:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "engine": ", ".join(r.get("engines", [])),
        })

    return {"success": True, "results": results, "query": query, "total_found": len(data.get("results", []))}


@server.tool()
def search_web(
    query: str,
    engines: list[str] | None = None,
    max_results: int = 10,
    language: str | None = None,
    categories: list[str] | None = None,
) -> dict:
    """Search the web via SearXNG. Optional: filter by engines, categories (general/news/images/science/files/social+media/videos)."""
    return _search(query, categories=categories, engines=engines, max_results=max_results, language=language)


@server.tool()
def search_news(query: str, max_results: int = 10) -> dict:
    """Search news articles via SearXNG."""
    return _search(query, categories=["news"], max_results=max_results)


@server.tool()
def search_images(query: str, max_results: int = 10) -> dict:
    """Search images via SearXNG. Returns title, URL, thumbnail, and source."""
    params = {"q": query, "format": "json", "categories": "images", "pageno": 1}

    try:
        resp = _get_client().get(f"{SEARXNG_URL}/search", params=params)
        resp.raise_for_status()
        data = resp.json()
    except httpx.ConnectError:
        return {"success": False, "error": "ECONNREFUSED", "detail": f"Cannot reach SearXNG at {SEARXNG_URL}"}
    except Exception as e:
        return {"success": False, "error": "EPROCESSING", "detail": str(e)}

    results = []
    for r in data.get("results", [])[:max_results]:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "thumbnail_url": r.get("thumbnail_src", r.get("img_src", "")),
            "source": r.get("source", ""),
        })

    return {"success": True, "results": results, "query": query}


@server.tool()
def list_engines(enabled_only: bool = True) -> dict:
    """List all available search engines from the SearXNG instance.
    
    Args:
        enabled_only: If True (default), return only enabled engines.
    """
    try:
        resp = _get_client().get(f"{SEARXNG_URL}/search", params={"format": "json", "q": "healthcheck"})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"success": False, "error": "ECONNREFUSED", "detail": str(e)}

    engines = []
    try:
        resp = _get_client().get(f"{SEARXNG_URL}/config")
        resp.raise_for_status()
        config = resp.json()
        for eng in config.get("engines", []):
            is_enabled = eng.get("enabled", False)
            if enabled_only and not is_enabled:
                continue
            engines.append({
                "name": eng.get("name", ""),
                "status": "enabled" if is_enabled else "disabled",
                "categories": eng.get("categories", []),
            })
    except Exception:
        pass

    if not engines:
        for eng_name, eng_data in data.get("engines", {}).items():
            engines.append({"name": eng_name, "status": "ok"})

    return {"success": True, "engines": engines}


def main():
    server.run()


if __name__ == "__main__":
    main()
