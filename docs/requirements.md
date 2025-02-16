# Agentic Backend

Create an MVP backend application demonstrating Agentic Workflows capabilities.

## Requirements

### General Requirements

1. Use Git for version control with atomic commits
2. Demonstrate good engineering practices (e.g., TDD)

### Technical Stack Requirements

#### Required Libraries

- Python >= 3.8
- FastAPI
- Pydantic
- Beanie
- Langgraph

#### Recommended Libraries

- Langchain OpenAI
- Langchain Community

#### Additional Technologies (Extra Consideration)

- Docker
- MongoDB
  - MongoDB docker image available

## Main Assignment Details

### Research Agent Implementation

Create a backend application managing a Research Agent that:

1. Pulls data from multiple sources
2. Synthesizes user-directed content
3. Uses tool/function calling for:
   - LLM determination of appropriate tools
   - Tool query generation
   - Query execution
   - Data synthesis

### Required Integrations

- LLM: OpenAI's GPT-4o-mini
- One or more of the following tools:
  - PubMed
  - Arxiv
  - Wikipedia
  - Web Search Engine (e.g., DuckDuckGo)

### Core Features

1. CRD (Create, Read, Delete) workflows for research agent
   - Store agent details in MongoDB
2. Handle prompt queries to research agent
   - Storage of prompt queries not required

### API Documentation

- OpenAPI documentation provided separately
- Document any design deviations in README.md

## Personalization Features

### Text Extraction Capabilities

1. File Types Support:
   - PDF (.pdf)
   - Word (.docx, .doc)
   - Excel (.xlsx, .xls)
   - PowerPoint (.ppt, .pptx)
2. Website Text Extraction
3. Text Tokenization
4. Optional: OCR for image text extraction

### Integration Requirements

1. Implement PUT endpoints:
   - /agents/{agent_id}/files
   - /agents/{agent_id}/websites
2. Token Management:
   - Enforce 120k token maximum context
   - Implement error handling for token limit exceeded

### Knowledge Base Integration

1. Incorporate as long-context in Research Agent's system prompt
2. Prioritize knowledge base over tool usage

### Additional Required Library

- Unstructured (for core functionality/partitioning)

Note: The assignment aims to demonstrate understanding of Agentic Workflows and ability to implement a practical research assistant system with optional personalization features.
