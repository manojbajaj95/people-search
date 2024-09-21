import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app, Person


def test_create_profile(client: TestClient, session: Session):
    response = client.post(
        "/api/person",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "profession": "Software Engineer",
            "location": "New York",
            "skills": ["Python", "FastAPI", "PostgreSQL"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "Python" in data["skills"]


def test_retrieve_profile(client: TestClient, session: Session):
    # First, create a profile
    create_response = client.post(
        "/api/person",
        json={
            "name": "Jane Smith",
            "email": "jane@example.com",
            "profession": "Data Scientist",
            "location": "San Francisco",
            "skills": ["Python", "Machine Learning", "SQL"]
        }
    )
    created_person = create_response.json()
    person_id = created_person["id"]

    # Now, retrieve the profile
    response = client.get(f"/api/person/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Smith"
    assert data["email"] == "jane@example.com"
    assert "Machine Learning" in data["skills"]


def test_update_profile(client: TestClient, session: Session):
    # First, create a profile
    create_response = client.post(
        "/api/person",
        json={
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "profession": "Web Developer",
            "location": "Chicago",
            "skills": ["JavaScript", "React", "Node.js"]
        }
    )
    created_person = create_response.json()
    person_id = created_person["id"]

    # Now, update the profile
    update_response = client.put(
        f"/api/person/{person_id}",
        json={
            "profession": "Full Stack Developer",
            "skills": ["JavaScript", "React", "Node.js", "Python", "Django"]
        }
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["profession"] == "Full Stack Developer"
    assert "Django" in updated_data["skills"]


def test_search_persons(client: TestClient, session: Session):
    # Create multiple profiles
    profiles = [
        {
            "name": "Alice Brown",
            "email": "alice@example.com",
            "profession": "UX Designer",
            "location": "London",
            "skills": ["UI/UX", "Figma", "Sketch"]
        },
        {
            "name": "Charlie Davis",
            "email": "charlie@example.com",
            "profession": "DevOps Engineer",
            "location": "Berlin",
            "skills": ["Docker", "Kubernetes", "AWS"]
        },
        {
            "name": "Eva Green",
            "email": "eva@example.com",
            "profession": "Data Engineer",
            "location": "Paris",
            "skills": ["Python", "Spark", "Hadoop"]
        }
    ]

    for profile in profiles:
        client.post("/api/person", json=profile)

    # Search for persons with Python skill
    response = client.get("/api/person", params={"skills": "Python"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(person["name"] == "Eva Green" for person in data)

    # Search for persons in London
    response = client.get("/api/person", params={"location": "London"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(person["name"] == "Alice Brown" for person in data)
