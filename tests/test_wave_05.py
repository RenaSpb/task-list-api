import pytest
from app.db import db
from app.models.goal import Goal

def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]

def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }

def test_get_goal_not_found(client):
    # Act
    response = client.get("/goals/999")  
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert response_body["message"] == "Goal 999 not found"

def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }

def test_update_goal(client, one_goal):
    # Act
    response = client.put("/goals/1", json={"title": "Updated Goal Title"})

    # Assert
    assert response.status_code == 204
    
    get_response = client.get("/goals/1")
    get_body = get_response.get_json()
    assert get_body == {
        "goal": {
            "id": 1,
            "title": "Updated Goal Title"
        }
    }

def test_update_goal_not_found(client):
    # Act
    response = client.put("/goals/999", json={"title": "Should Not Exist"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body["message"] == "Goal 999 not found"

def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")

    # Assert
    assert response.status_code == 204

    query = db.select(Goal).where(Goal.id == 1)
    assert db.session.scalar(query) == None

def test_delete_goal_not_found(client):

    # Act
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Goal 1 not found"}


def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
