"""
Tests for Flask application routes and API endpoints.
"""

import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_sample_route(client):
    response = client.get("/samples/identical")
    assert response.status_code == 200
    data = response.get_json()
    assert "The Knuth-Morris-Pratt" in data["doc1"]

    not_found = client.get("/samples/invalid_sample")
    assert not_found.status_code == 404


def test_api_compare_success(client):
    payload = {
        "doc1_text": "Knuth-Morris-Pratt algorithm searches for occurrences of a pattern within text.",
        "doc2_text": "Knuth-Morris-Pratt algorithm searches for occurrences of a pattern within text.",
        "algorithm": "kmp",
        "shingle_size": 4
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["similarity_percentage"] == 100.0
    assert "benchmark" in data["data"]


def test_api_compare_empty_validation(client):
    payload = {"doc1_text": "", "doc2_text": ""}
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 400
