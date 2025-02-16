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

3. Run the server for development:

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

   - Instead of using a JSON string for `agent_post`, the `name` field is a required Form during agent creation
   - Returns ID of agent document

3. Knowledge base

   - Uses a SHA256 hashing to prevent duplicate file processing. The files are stored as ID references in `agent.files`. If the file has been uploaded before, the previous copy's ID will be appended to the agent's file list.
   - Similarly, websites are cleaned with `courlan` and the URLs stored in `File.name` to prevent saving duplicate links.
   - Adds a `created_at` field to track when a file was added

4. `File` and `Website` are defined within the same model but they should rightfully be stored separately. The website scraping (performed with `unstructured`) logic is currently rudimentary and should be further expanded on in the future, such as by identifying `NarrativeText` type elements and removing large whitespaces.

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
