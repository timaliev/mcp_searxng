# mcp_searxng

MCP server for privacy-respecting web search via [SearXNG](https://github.com/searxng/searxng).

> **Requires [pi-mcp-bridge](https://github.com/timaliev/pi-mcp-bridge)** to connect to [pi](https://pi.dev).

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
        },
        "setupCommands": [
          "uv tool install --python 3.11 git+https://github.com/timaliev/mcp_searxng.git"
        ],
        "githubRepo": "timaliev/mcp_searxng",
        "versionCommand": "mcp-searxng --version"
      }
    ]
  }
}
```

### Standalone MCP client

In `~/.mcp.json`:

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

## Error Handling

All tools return a structured response with a `success` field. If SearXNG is unreachable or returns an error, `success` will be `false` with an error code and detail:

| Error Code | Cause |
|------------|-------|
| `ECONNREFUSED` | SearXNG instance is not running or not reachable at the configured `SEARXNG_URL` |
| `ESEARCH` | SearXNG returned an HTTP error (e.g., 500) |
| `EPROCESSING` | Unexpected error while processing the request |

Example error response:

```json
{
  "success": false,
  "error": "ECONNREFUSED",
  "detail": "Cannot reach SearXNG at http://localhost:8080/searxng"
}
```

The server does **not** crash or exit — errors are returned inline so the agent can handle them gracefully.

## Development

```bash
git clone https://github.com/timaliev/mcp_searxng.git
cd mcp_searxng
uv run mcp-searxng
```
