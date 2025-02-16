import io

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


@pytest.fixture(scope="module")
def settings():
    return get_settings()


@pytest.fixture(scope="module")
def test_client(settings):
    with TestClient(app) as client:
        yield client


def test_create_agent(test_client):
    data = {"name": "TestAgent"}
    response = test_client.post("/agents", data=data)
    assert response.status_code == 201
    json_data = response.json()
    # Expecting a response of the form {"id": "<agent_id>"}
    assert "id" in json_data
    id = json_data["id"]
    test_client.delete(f"/agents/{id}")


def test_get_all_agents(test_client):
    response = test_client.get("/agents")
    assert response.status_code == 200
    agents = response.json()
    assert isinstance(agents, list)


def test_create_get_and_delete_agent(test_client):
    data = {"name": "TempAgent"}
    response = test_client.post("/agents", data=data)
    assert response.status_code == 201
    agent_id = response.json()["id"]

    response = test_client.get(f"/agents/{agent_id}")
    assert response.status_code == 200
    agent = response.json()
    assert agent["name"] == "TempAgent"

    response = test_client.delete(f"/agents/{agent_id}")
    assert response.status_code == 204

    response = test_client.get(f"/agents/{agent_id}")
    assert response.status_code == 404


def test_update_agent_websites(test_client):
    data = {"name": "WebAgent", "prompt": "Default prompt"}
    response = test_client.post("/agents", data=data)
    agent_id = response.json()["id"]

    websites = ["https://fastapi.tiangolo.com/tutorial/testing/#extended-testing-file"]
    response = test_client.put(f"/agents/{agent_id}/websites", json=websites)
    assert response.status_code == 204

    response = test_client.get(f"/agents/{agent_id}")
    assert response.status_code == 200

    agent = response.json()
    assert "files" in agent
    assert len(agent["files"]) > 0
    test_client.delete(f"/agents/{agent_id}")


def test_update_agent_files(test_client):
    data = {"name": "FileAgent", "prompt": "Default prompt"}
    response = test_client.post("/agents", data=data)
    agent_id = response.json()["id"]

    with open("tests/docs/Resume.pdf", "rb") as f:
        file_content = f.read()
    files = [("files", ("Resume.pdf", io.BytesIO(file_content), "application/pdf"))]
    response = test_client.put(f"/agents/{agent_id}/files", files=files)
    assert response.status_code == 204

    response = test_client.get(f"/agents/{agent_id}")
    assert response.status_code == 200
    agent = response.json()
    assert "files" in agent
    assert any("Resume.pdf" in f.get("name", "") for f in agent["files"])
    test_client.delete(f"/agents/{agent_id}")


def test_send_message(test_client):
    # Create an agent to send a query
    data = {"name": "QueryAgent", "prompt": "Default prompt"}
    response = test_client.post("/agents", data=data)
    agent_id = response.json()["id"]

    # Send a research query message
    payload = {"message": "What is the capital of France?"}
    response = test_client.post(f"/agents/{agent_id}/queries", json=payload)
    # Since the LLM and tool integration are active, we expect a 201 response
    assert response.status_code == 201
    result = response.json()
    assert isinstance(result, dict)
    assert "messages" in result
    test_client.delete(f"/agents/{agent_id}")
