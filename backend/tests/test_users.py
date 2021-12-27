import pytest

TEST_USERNAMES = ["johnsmith", "😀"]

TEST_USER_DATA = [("johnsmith", "john", "smith"), ("😀", "happy", "face")]


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
    assert res.status_code == expected_status_code


@pytest.mark.parametrize("username", TEST_USERNAMES)
def test_get_non_existing_user(client, username):
    res = client.get(f"/user?username={username}")
    assert res.status_code == 404


@pytest.mark.parametrize("username,first_name,last_name", TEST_USER_DATA)
def test_get_existing_user(client, username, first_name, last_name):
    client.post(
        "/user",
        json={"username": username, "first_name": first_name, "last_name": last_name},
    )
    res = client.get(f"/user?username={username}")
    assert res.json["user"]["username"] == username
    assert res.json["user"]["first_name"] == first_name
    assert res.json["user"]["last_name"] == last_name
    assert res.status_code == 200


@pytest.mark.parametrize("username", TEST_USERNAMES)
def test_delete_non_existing_user(client, username):
    res = client.delete(f"/user?username={username}")
    assert res.status_code == 204


@pytest.mark.parametrize("username,first_name,last_name", TEST_USER_DATA)
def test_delete_existing_user(client, username, first_name, last_name):
    client.post(
        "/user",
        json={"username": username, "first_name": first_name, "last_name": last_name},
    )
    res = client.delete(f"/user?username={username}")
    assert res.status_code == 200


@pytest.mark.parametrize("username,first_name,last_name", TEST_USER_DATA)
def test_create_user(client, username, first_name, last_name):
    res = client.post(
        "/user",
        json={"username": username, "first_name": first_name, "last_name": last_name},
    )
    assert res.json["user"]["username"] == username
    assert res.json["user"]["first_name"] == first_name
    assert res.json["user"]["last_name"] == last_name
    assert res.status_code == 200


@pytest.mark.parametrize("username,first_name,last_name", TEST_USER_DATA)
def test_crd_user(client, username, first_name, last_name):
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

    res = client.delete(f"/user?username={username}")
    assert res.status_code == 200

    res = client.get(f"/user?username={username}")
    assert res.status_code == 404
