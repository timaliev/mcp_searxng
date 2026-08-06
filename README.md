# mcp_searxng

MCP server for privacy-respecting web search via [SearXNG](https://github.com/searxng/searxng).

> **Requires [pi-mcp-bridge](https://github.com/timaliev/pi-mcp-bridge)** to connect to pi.

## Prerequisites

- SearXNG instance running (default: `http://localhost:8080/searxng`)

## Installation

```bash
pip install git+https://github.com/timaliev/mcp_searxng.git
```

Or via uv:

```bash
uv tool install git+https://github.com/timaliev/mcp_searxng.git
```

## Configuration

### With pi-mcp-bridge

In `~/.pi/agent/settings.json`:

```json
{
  "mcpBridge": {
    "servers": [
      {
        "name": "searxng",
        "command": "mcp-searxng",
        "args": [],
        "env": {
          "SEARXNG_URL": "http://localhost:8080/searxng"
        }
      }
    ]
  }
}
```

### Standalone MCP client

```json
{
  "mcpServers": {
    "searxng": {
      "command": "mcp-searxng",
      "args": [],
      "env": {
        "SEARXNG_URL": "http://localhost:8080/searxng"
      }
    }
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SEARXNG_URL` | `http://localhost:8080/searxng` | SearXNG instance URL |

## Tools

| Tool | Description |
|------|-------------|
| `search_web` | Web search with engine/category/language filters |
| `search_news` | News-only search |
| `search_images` | Image search with thumbnails |
| `list_engines` | List available/enabled SearXNG engines |

## Development

```bash
git clone https://github.com/timaliev/mcp_searxng.git
cd mcp_searxng
uv run mcp-searxng
```
