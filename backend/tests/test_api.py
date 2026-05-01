import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_create_experiment(client, auth_headers):
    response = await client.post(
        "/api/v1/experiments/",
        json={
            "name": "Test Imaging Experiment",
            "description": "Testing M. abscessus under amikacin",
            "experiment_type": "imaging",
            "replicates": 3,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Imaging Experiment"
    assert data["experiment_type"] == "imaging"
    assert data["status"] == "created"


@pytest.mark.asyncio
async def test_list_experiments(client, auth_headers):
    # Create an experiment first
    await client.post(
        "/api/v1/experiments/",
        json={"name": "Test Exp", "experiment_type": "crispr"},
        headers=auth_headers,
    )
    response = await client.get("/api/v1/experiments/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "experiments" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_get_experiment(client, auth_headers):
    create_resp = await client.post(
        "/api/v1/experiments/",
        json={"name": "Get Test", "experiment_type": "tnseq"},
        headers=auth_headers,
    )
    exp_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/experiments/{exp_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == exp_id


@pytest.mark.asyncio
async def test_update_experiment(client, auth_headers):
    create_resp = await client.post(
        "/api/v1/experiments/",
        json={"name": "Update Test", "experiment_type": "imaging"},
        headers=auth_headers,
    )
    exp_id = create_resp.json()["id"]
    response = await client.put(
        f"/api/v1/experiments/{exp_id}",
        json={"name": "Updated Name", "notes": "Updated notes"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_experiment(client, auth_headers):
    create_resp = await client.post(
        "/api/v1/experiments/",
        json={"name": "Delete Test", "experiment_type": "tnseq"},
        headers=auth_headers,
    )
    exp_id = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/experiments/{exp_id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_create_strain(client, auth_headers):
    response = await client.post(
        "/api/v1/experiments/strains",
        json={
            "name": "ATCC 19977",
            "subspecies": "abscessus",
            "source": "ATCC",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "ATCC 19977"


@pytest.mark.asyncio
async def test_create_drug(client, auth_headers):
    response = await client.post(
        "/api/v1/experiments/drugs",
        json={
            "name": "Amikacin",
            "drug_class": "aminoglycoside",
            "mic_reference": 16.0,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Amikacin"
