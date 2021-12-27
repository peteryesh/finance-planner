import pytest


@pytest.mark.parametrize(
    "username,first_name,last_name,expected_status_code",
    [("", "john", "smith", 400), (None, "john", "smith", 400)],
)
def test_bad_post_requests(
    client, username, first_name, last_name, expected_status_code
):
    res = client.post(
        "/user",
        json={"username": username, "first_name": first_name, "last_name": last_name},
    )
    print(res.status_code)
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    "username,first_name,last_name",
    [
        ("johnsmith", "john", "smith"),
    ],
)
def test_post_and_get_user(client, username, first_name, last_name):
    res = client.post(
        "/user",
        json={"username": username, "first_name": first_name, "last_name": last_name},
    )
    assert res.json["user"]["username"] == username
    assert res.json["user"]["first_name"] == first_name
    assert res.json["user"]["last_name"] == last_name
    assert res.status_code == 200

    res = client.get(f"/user?username={username}")
    assert res.json["user"]["username"] == username
    assert res.json["user"]["first_name"] == first_name
    assert res.json["user"]["last_name"] == last_name
    assert res.status_code == 200
