from fastapi.testclient import TestClient


def test_fail_get_teams(client: TestClient) -> None:
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == {
        "message": "No teams found",
        "status": "success",
        "data": None
    }

def test_fail_get_team(client: TestClient) -> None:
    response = client.get("/teams/ash")
    assert response.status_code == 400
    assert response.json() == {
        "message": "Trainer ash not found",
        "status": "error",
        "data": None
    }

def test_fail_create_team(client: TestClient) -> None:
    response = client.post("/teams", json={
        "user": "ash",
        "team": []
    })
    assert response.status_code == 400
    assert response.json() == {
        "message": "Error creating team, team is empty",
        "status": "error",
        "data": None
    }

def test_fail_create_team_pokemon_not_found(client: TestClient) -> None:
    response = client.post("/teams", json={
        "user": "ash",
        "team": ["picachu", "charmander"]
    })
    assert response.status_code == 400
    assert response.json() == {
        "message": "Error creating team, pokemon picachu not found",
        "status": "error",
        "data": None
    }

def test_create_team(client: TestClient) -> None:
    response = client.post("/teams", json={
        "user": "ash",
        "team": ["pikachu", "charmander"]
    })
    assert response.status_code == 201
    assert response.json() == {
        "message": "Team created successfully",
        "status": "success",
        'data': {
            'owner': 'ash',
            'pokemons': [{
                'height': 4,
                'id': 1,
                'name': 'pikachu',
                'weight': 60},
                {
                'height': 6,
                'id': 2,
                'name': 'charmander',
                'weight': 85
                }]},
            }

def test_get_teams(client: TestClient) -> None:
    response = client.get("/teams/ash")
    assert response.status_code == 200
    assert response.json() == {
            "owner": "ash",
            "pokemons": [
                {
                    "height": 4,
                    "id": 1,
                    "name": "pikachu",
                    "weight": 60
                },
                {
                    "height": 6,
                    "id": 2,
                    "name": "charmander",
                    "weight": 85
                }
            ]
        }

def test_get_teams(client: TestClient) -> None:
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == {
            '1': {
                "owner": "ash",
                "pokemons": [
                    {
                        "height": 4,
                        "id": 1,
                        "name": "pikachu",
                        "weight": 60
                    },
                    {
                        "height": 6,
                        "id": 2,
                        "name": "charmander",
                        "weight": 85
                    }
                ]
            }
        }
