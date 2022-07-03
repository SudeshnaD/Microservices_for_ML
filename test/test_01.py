import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import json

client = TestClient(app)

def test_valid_employee_name():
    print(os.getcwd())
    print("here here")
    response = client.get("/api/employees/name=Gail")
    responsedict = json.loads(response.json())
    assert response.status_code == 200
    assert "Gail" in responsedict["name"] and "USA" in responsedict["address"]["Country"] and "gail@kitty.com" in responsedict["email"]


def test_invalid_input():
    response = client.get("/api/employees/name=XYZ")
    assert response.status_code == 500
    assert response.json() == {'detail': 'Name not found'}



