"""
Tests for the root endpoint.
"""
import pytest


def test_root_endpoint(client):
    """Test the root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Blog API running"}


def test_docs_endpoint(client):
    """Test that docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
