"""Tests for list-endpoint pagination (Task #8)."""


def _seed_notes(client, count: int):
    """Helper – create *count* notes and return their IDs."""
    ids = []
    for i in range(1, count + 1):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Body {i}"})
        ids.append(r.json()["data"]["id"])
    return ids


def _seed_action_items(client, count: int):
    """Helper – create *count* action items and return their IDs."""
    ids = []
    for i in range(1, count + 1):
        r = client.post("/action-items/", json={"description": f"Item {i}"})
        ids.append(r.json()["data"]["id"])
    return ids


# ── Notes pagination ────────────────────────────────────────────────


def test_notes_default_pagination(client):
    """Default page=1, page_size=10 should return up to 10 items."""
    _seed_notes(client, 3)
    r = client.get("/notes/")
    body = r.json()
    assert r.status_code == 200
    data = body["data"]
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_notes_custom_page_size(client):
    """page_size=2 should limit items per page."""
    _seed_notes(client, 5)

    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    data = r.json()["data"]
    assert data["total"] == 5
    assert len(data["items"]) == 2

    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    data = r.json()["data"]
    assert len(data["items"]) == 2

    r = client.get("/notes/", params={"page": 3, "page_size": 2})
    data = r.json()["data"]
    assert len(data["items"]) == 1


def test_notes_empty_last_page(client):
    """Requesting a page beyond total should return empty items but correct total."""
    _seed_notes(client, 2)
    r = client.get("/notes/", params={"page": 99, "page_size": 10})
    data = r.json()["data"]
    assert data["total"] == 2
    assert data["items"] == []


def test_notes_empty_database(client):
    """No notes at all – total=0, items=[]."""
    r = client.get("/notes/")
    data = r.json()["data"]
    assert data["total"] == 0
    assert data["items"] == []


def test_notes_page_size_larger_than_total(client):
    """page_size bigger than total should just return all items."""
    _seed_notes(client, 3)
    r = client.get("/notes/", params={"page_size": 100})
    data = r.json()["data"]
    assert data["total"] == 3
    assert len(data["items"]) == 3


# ── Action-items pagination ─────────────────────────────────────────


def test_action_items_default_pagination(client):
    _seed_action_items(client, 4)
    r = client.get("/action-items/")
    data = r.json()["data"]
    assert data["total"] == 4
    assert len(data["items"]) == 4


def test_action_items_custom_page_size(client):
    _seed_action_items(client, 5)

    r = client.get("/action-items/", params={"page": 1, "page_size": 3})
    data = r.json()["data"]
    assert data["total"] == 5
    assert len(data["items"]) == 3

    r = client.get("/action-items/", params={"page": 2, "page_size": 3})
    data = r.json()["data"]
    assert len(data["items"]) == 2


def test_action_items_empty_last_page(client):
    _seed_action_items(client, 2)
    r = client.get("/action-items/", params={"page": 50})
    data = r.json()["data"]
    assert data["total"] == 2
    assert data["items"] == []


def test_action_items_empty_database(client):
    r = client.get("/action-items/")
    data = r.json()["data"]
    assert data["total"] == 0
    assert data["items"] == []


def test_action_items_page_size_larger_than_total(client):
    _seed_action_items(client, 2)
    r = client.get("/action-items/", params={"page_size": 100})
    data = r.json()["data"]
    assert data["total"] == 2
    assert len(data["items"]) == 2
