def test_post_and_get_user(client):
    res = client.post(
        "/user",
        json={"username": "johnsmith", "first_name": "john", "last_name": "smith"},
    )
    assert res.json["user"]["username"] == "johnsmith"
    assert res.json["user"]["first_name"] == "john"
    assert res.json["user"]["last_name"] == "smith"

    res = client.get("/user?username=johnsmith")
    assert res.json["user"]["username"] == "johnsmith"
    assert res.json["user"]["first_name"] == "john"
    assert res.json["user"]["last_name"] == "smith"
