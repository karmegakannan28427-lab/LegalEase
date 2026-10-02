"""
Basic backend tests for LegalEase.
"""

import os


# Use demo mode for testing
os.environ["DEMO_MODE"] = "true"

os.environ.pop(
    "GEMINI_API_KEY",
    None
)


from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.json()["service"]
        == "LegalEase"
    )


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "healthy"
    )


def test_generate_demo_document():

    payload = {

        "document_type":
            "Non-Disclosure Agreement",

        "parties":
            "Alice (Disclosing Party), "
            "Example Corp (Receiving Party)",

        "terms":
            "Protect confidential information;"
            "No third-party disclosure;"
            "Term is two years",

        "dates":
            "October 2, 2026",
    }


    response = client.post(
        "/generate",
        json=payload
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["document_type"]
        == payload["document_type"]
    )


    assert (
        "NON-DISCLOSURE AGREEMENT"
        in data["generated_text"]
    )


    assert (
        "confidential"
        in data["generated_text"].lower()
    )