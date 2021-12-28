import pytest

TEST_USER_DATA = [("johnsmith", "john", "smith"), ("janeparker", "jane", "parker")]

TEST_ACCT_DATA = [
    ("107db7f2-ab28-4d92-9830-9ab0af34cfb3", 1, "John Checking", 5167.83, "johnsmith"),
    (
        "070bf38e-65ba-477a-87ca-711bfd0d7fd2",
        7,
        "Jane TD Ameritrade",
        13200.65,
        "janesmith",
    ),
]

TEST_NEW_ACCT_DATA = [
    ("", 1, "John Checking", 5167.83, "johnsmith"),
    (
        None,
        7,
        "Jane TD Ameritrade",
        13200.65,
        "janesmith",
    ),
]


@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 1, "Checking", 500.00, ""),
        ("070bf38e-65ba-477a-87ca-711bfd0d7fd2", 1, "Checking", 500.00, None),
    ],
)
def test_account_post_missing_username(
    client,
    account_id,
    account_type,
    account_name,
    account_balance,
    username,
):
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    assert res.status_code == 400


## Expected result: Create account row with new uuid
@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username",
    [
        ("", 1, "Checking", 500.00, "johnsmith"),
        (None, 1, "Checking", 500.00, "janesmith"),
    ],
)
def test_new_account_id(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post(
        "/user",
        json={"username": username, "first_name": "", "last_name": ""},
    )
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    assert res.status_code == 201
    assert len(res.json["account"]["account_id"]) == 36
    assert res.json["account"]["account_type"] == account_type
    assert res.json["account"]["account_name"] == account_name
    assert res.json["account"]["account_balance"] == account_balance
    assert res.json["account"]["username"] == username


@pytest.mark.parametrize(
    "account_id,username",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", "johnsmith"),
        ("070bf38e-65ba-477a-87ca-711bfd0d7fd2", "janesmith"),
    ],
)
def test_post_invalid_account_id(client, account_id, username):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": 1,
            "account_name": "",
            "account_balance": "",
            "username": username,
        },
    )
    assert res.status_code == 400


@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username", TEST_NEW_ACCT_DATA
)
def test_post_valid_account_id(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    init_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    res = client.post(
        "/account",
        json={
            "account_id": init_res.json["account"]["account_id"],
            "account_type": account_type + 2,
            "account_name": account_name + "test string addition",
            "account_balance": account_balance - 5000,
            "username": username,
        },
    )
    assert res.status_code == 200
    assert len(res.json["account"]["account_id"]) == 36
    assert res.json["account"]["account_type"] == account_type + 2
    assert res.json["account"]["account_name"] == account_name + "test string addition"
    assert res.json["account"]["account_balance"] == account_balance - 5000
    assert res.json["account"]["username"] == username


@pytest.mark.parametrize(
    "account_id, account_type, username",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 0, "johnsmith"),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 10, "johnsmith"),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", -1, "johnsmith"),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", None, "johnsmith"),
    ],
)
def test_account_type_invalid(client, account_id, account_type, username):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "username": username,
        },
    )
    assert res.status_code == 400


@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username",
    [
        ("", 1, "", 500.00, "johnsmith"),
        ("", 1, None, 500.00, "janesmith"),
        (None, 1, "", 500.00, "johnsmith"),
        (None, 1, None, 500.00, "janesmith"),
    ],
)
def test_account_name_missing(
    client,
    account_id,
    account_type,
    account_name,
    account_balance,
    username,
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    assert res.status_code == 201
    assert res.json["account"]["account_name"] == "Squirtle is lucky"


@pytest.mark.parametrize(
    "account_id, account_type, account_balance, username",
    [
        ("", 1, None, "johnsmith"),
    ],
)
def test_account_balance_missing_on_creation(
    client, account_id, account_type, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": "",
            "account_balance": account_balance,
            "username": username,
        },
    )
    assert res.status_code == 201
    assert res.json["account"]["account_balance"] == 0


@pytest.mark.parametrize(
    "account_id, account_type, account_name, account_balance, username",
    TEST_NEW_ACCT_DATA,
)
def test_get_account_success(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    acct_id = post_res.json["account"]["account_id"]
    res = client.get(f"/account?account_id={acct_id}&username={username}")
    assert res.status_code == 200
    assert len(res.json["account"]["account_id"]) == 36
    assert res.json["account"]["account_id"] == acct_id
    assert res.json["account"]["account_type"] == account_type
    assert res.json["account"]["account_name"] == account_name
    assert res.json["account"]["account_balance"] == account_balance
    assert res.json["account"]["username"] == username


@pytest.mark.parametrize(
    "account_id, account_type, account_name, account_balance, username", TEST_ACCT_DATA
)
def test_get_account_failure(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.get(f"/account?account_id={account_id}&username={username}")
    assert res.status_code == 400


@pytest.mark.parametrize(
    "account_id, account_type, account_name, account_balance, username",
    TEST_NEW_ACCT_DATA,
)
def test_delete_account_success(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "account_name": account_name,
            "account_balance": account_balance,
            "username": username,
        },
    )
    acct_id = post_res.json["account"]["account_id"]
    res = client.delete(f"/account?account_id{acct_id}&username={username}")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "account_id, account_type, account_name, account_balance, username", TEST_ACCT_DATA
)
def test_delete_account_success(
    client, account_id, account_type, account_name, account_balance, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.delete(f"/account?account_id{account_id}&username={username}")
    assert res.status_code == 400
