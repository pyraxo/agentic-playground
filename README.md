# Agentic Playground

## Installation

1. Ensure you have [uv](https://docs.astral.sh/uv/) and Python 3.10+ installed. The `.python-version` file tells `uv` which Python version to install and use when running this project.

2. Create a virtual environment and activate it:

```sh
uv venv
source .venv/bin/activate
```

3. Copy `.env.example` into `.env` and fill in `OPENAI_API_KEY`:

```sh
cp .env.example .env
nano .env
```

3. Run the server for development:

```sh
uv run fastapi dev
```
