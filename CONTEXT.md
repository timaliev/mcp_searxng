# CONTEXT.md — Glossary for mcp_searxng

## Domain

- **MCP (Model Context Protocol)** — JSON-RPC protocol connecting AI agents to tools over stdio/SSE
- **SearXNG** — privacy-respecting metasearch engine, self-hosted, aggregates results from multiple search engines
- **Engine** — individual search backend within SearXNG (Google, DuckDuckGo, Brave, etc.)

## Architecture

- `mcp_searxng/server.py` — single-file MCP server
- Communicates with SearXNG JSON API over HTTP
- Four tools: `search_web`, `search_news`, `search_images`, `list_engines`
- Configured via `SEARXNG_URL` env var (default: `http://localhost:8080/searxng`)

## Conventions

- **Language:** Python 3.11+
- **Package manager:** uv / pip
- **Testing:** pytest (to be added)
- **CI/CD:** GitHub Actions (to be added)
- **Versioning:** semantic via git-cliff
