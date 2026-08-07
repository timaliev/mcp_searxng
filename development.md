# Development — mcp_searxng

## Setup

```bash
git clone https://github.com/timaliev/mcp_searxng.git
cd mcp_searxng
uv sync
```

## Prerequisites

- SearXNG instance running (default: `http://localhost:8080/searxng`)

## Run

```bash
uv run mcp-searxng
```

## Linting & formatting

```bash
uv run ruff check .          # lint
uv run ruff check --fix .    # auto-fix
uv run ruff format .         # format
```

## Git workflow

- NEVER work directly on `develop` or `master`
- Create feature branch from `develop`: `git checkout -b feat/my-feature develop`
- Commit using [conventional commits](https://www.conventionalcommits.org/)
- Open PR to `develop`
- Release: merge `develop` → `release` → PR → `master` (GitHub Actions handles tags + CHANGELOG)
