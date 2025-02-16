# Agentic Playground

## Local installation

Ensure you have [uv](https://docs.astral.sh/uv/) and Python 3.11 installed. The `.python-version` file tells `uv` which Python version to install and use when running this project.

Later Python versions cause `unstructured-inference` to throw errors (tested on 3.13).

1. Create a virtual environment and activate it:

```sh
uv venv
source .venv/bin/activate
```

2. Copy `.env.example` into `.env` and fill in the required environment variables:

```sh
cp .env.example .env
nano .env
```

- `OPENAI_API_KEY`: Your OpenAI API key (found [here](https://platform.openai.com/api-keys))
- `MONGO_URI`: MongoDB connection string (e.g., `mongodb://localhost:27017`)
- `MONGO_DB_NAME`: Database name (default: `agent_workflow`)

3. [Unstructured](https://docs.unstructured.io/open-source/installation/full-installation) has many required dependencies to get OCR and document extraction working.

- `poppler` (for PDFs):

```sh
choco install poppler         # Windows
brew install poppler          # macOS
apt install -y poppler-utils
```

- `libmagic`, `libreoffice`, `pandoc`, `tesseract` are the other required libraries, and installing the Python wrappers may or may not suffice. If all else fails, use the Docker installation.

4. Run the server for development:

```sh
uv run fastapi dev
```

### Running tests

You can run the test suite using `pytest` with `--dev` dependencies installed:

```sh
pytest -v
```

Swagger docs can be found at the `/docs` endpoint, e.g. <http://localhost:8000/docs>.

## Docker installation

With [Docker Compose](https://docs.docker.com/compose/install/) installed, you can start the project with:

```sh
docker compose up --build
```

## API Reference

### Endpoints

- `GET /agents` - Get all agents
- `POST /agents` - Create a new research agent
- `GET /agents/{agent_id}` - Retrieve agent details
- `DELETE /agents/{agent_id}` - Delete an agent
- `POST /agents/{agent_id}/queries` - Send research queries to agent
- `PUT /agents/{agent_id}/websites` - Add website content to agent's knowledge base
- `PUT /agents/{agent_id}/files` - Add file content to agent's knowledge base

### Design Implementation

1. Added endpoint to view all agents (not in spec)

2. Agent creation (`POST /agents`)

   - Instead of supplying an object/string in `agent_post`, the request form can be supplied with `name`, `prompt` (both `str`), `files` (`list[UploadFile]`) and `websites` (`list[str]`). They are not required. See the Swagger docs for more info
   - Returns ID of agent document

3. Knowledge base

   - Uses a SHA256 hashing to prevent duplicate file processing. The files are stored as ID references in `agent.files`. If the file has been uploaded before, the previous copy's ID will be appended to the agent's file list.
   - Similarly, websites are cleaned with `courlan` and the URLs stored in `File.name` to prevent saving duplicate links.
   - Adds a `created_at` field to track when a file was added

### Project Structure

```
.
├── app/                   # Main application directory
│   ├── agents/            # Agent implementations and behaviors
│   ├── api/               # FastAPI route definitions
│   ├── models/            # Database models (Beanie/MongoDB)
│   ├── schemas/           # Pydantic schemas for request/response
│   ├── services/          # Business logic and service layer
│   └── main.py            # FastAPI application entry point
├── docs/                  # Project documentation
├── tests/                 # Test suite
└── README.md              # Project documentation
```

### Further improvements

1. `File` and `Website` are defined within the same model but they should be stored separately. The website scraping logic is currently rudimentary and should be further expanded on in the future, such as by only using `NarrativeText` type elements or removing large whitespaces.

2. OCR and text extraction are supported by `unstructured` but can be tweaked further with individual logic per file type.

3. While uploading files/websites, if the total number of tokens of an agent's knowledge base exceeds 120k, an error is raised. GPT-4o-mini's max input context window is 128k, so the 8k difference is reasonable. As we can supply the agents custom prompts that may exceed 8k, the custom prompt length should be taken into account as well.
