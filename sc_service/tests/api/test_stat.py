import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_stat(
    fx_client: AsyncClient
):
    data = [
        {
            "date": "2023-01-01",
            "views": 3,
            "clicks": 6,
            "cost": 100.99
        },{
            "date": "2023-01-02",
            "views": 10,
            "clicks": 2,
            "cost": 120.35
        },{
            "date": "2022-01-02",
            "views": 100,
            "clicks": 23,
            "cost": 1200.0
        },{
            "date": "2022-01-02",
            "views": 200,
            "clicks": 230,
            "cost": 50.0
        }
    ]
    for d in data:
        resp = await fx_client.post("/api/v1/stat", json=d)
        assert resp.status_code == 201

    resp = await fx_client.get("/api/v1/stat")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2023-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=date")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2022-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=views")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2023-01-01" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=-views")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2022-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=clicks")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2023-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=-clicks")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2022-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=cost")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2023-01-01" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=-cost")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2022-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=cpc")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2022-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=-cpc")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert "2023-01-02" == resp_dat["items"][0].get("date")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=cpm")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert 300 == resp_dat["items"][0].get("views")
    assert 3 == resp_dat["total"]

    resp = await fx_client.get("/api/v1/stat?orders=-cpm")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert 4160.0 == resp_dat["items"][2].get("cpm")
    assert 3 == resp_dat["total"]
    resp = await fx_client.get("/api/v1/stat?orders=-cpm&date_from=2022-01-02&date_to=2022-01-10")
    resp_dat = resp.json()
    assert resp.status_code == 200
    assert 1 == resp_dat["total"]

    resp = await fx_client.delete("/api/v1/stat")
    assert resp.status_code == 204
    resp = await fx_client.get("/api/v1/stat")
    assert resp.status_code == 200
    resp_dat = resp.json()
    assert 0 == resp_dat["total"]


@pytest.mark.anyio
async def test_unauthorized(
    fx_client_unauth: AsyncClient
):
    resp = await fx_client_unauth.get("/api/v1/stat")
    assert resp.status_code == 401

@pytest.mark.anyio
async def test_stat_inavlide_date(
    fx_client: AsyncClient
):
    data = [
        {
            "views": 3,
            "clicks": 6,
            "cost": 100.99
        }, {
            "date": "2023-01-02",
            "views": "sss10",
            "clicks": "dsdsd",
            "cost": "dsdsd"
        }, {}, {
            "date": None,
            "views": None,
            "clicks": None,
            "cost": None
        }
    ]

    for d in data:
        resp = await fx_client.post("/api/v1/stat", json=d)
        assert resp.status_code == 400

    resp = await fx_client.get("/api/v1/stat?orders=cpmdff")
    assert resp.status_code == 400

    resp = await fx_client.get("/api/v1/stat?date_from=cpmdff, date_to=ksmnksms")
    assert resp.status_code == 400