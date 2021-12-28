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


@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username,expected_status_code",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 1, "Checking", 500.00, "", 400),
        ("070bf38e-65ba-477a-87ca-711bfd0d7fd2", 1, "Checking", 500.00, None, 400),
    ],
)
def test_account_post_missing_username(
    client,
    account_id,
    account_type,
    account_name,
    account_balance,
    username,
    expected_status_code,
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
    assert res.status_code == expected_status_code


## Expected result: Create account row with new uuid
@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username,expected_status_code",
    [
        ("", 1, "Checking", 500.00, "johnsmith", 200),
        (None, 1, "Checking", 500.00, "janesmith", 200),
    ],
)
def test_new_account_id(
    client,
    account_id,
    account_type,
    account_name,
    account_balance,
    username,
    expected_status_code,
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
    assert res.status_code == expected_status_code
    assert len(res.json["account"]["account_id"]) == 36
    assert res.json["account"]["account_type"] == account_type
    assert res.json["account"]["account_name"] == account_name
    assert res.json["account"]["account_balance"] == account_balance
    assert res.json["account"]["username"] == username


@pytest.mark.parametrize(
    "account_id,username,expected_status_code",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", "johnsmith", 204),
        ("070bf38e-65ba-477a-87ca-711bfd0d7fd2", "janesmith", 204),
    ],
)
def test_post_invalid_account_id(client, account_id, username, expected_status_code):
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
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    "account_id, account_type, username, expected_status_code",
    [
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 0, "johnsmith", 400),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", 10, "johnsmith", 400),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", -1, "johnsmith", 400),
        ("a58273f4-ed75-419d-b4c6-ecd38d0571c6", None, "johnsmith", 400),
    ],
)
def test_account_type_invalid(
    client, account_id, account_type, username, expected_status_code
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": account_type,
            "username": username,
        },
    )
    assert res.status_code == expected_status_code


@pytest.mark.parametrize(
    "account_id,account_type,account_name,account_balance,username,expected_status_code",
    [
        ("", 1, "", 500.00, "johnsmith", 200),
        ("", 1, None, 500.00, "janesmith", 200),
        (None, 1, "", 500.00, "johnsmith", 200),
        (None, 1, None, 500.00, "janesmith", 200),
    ],
)
def test_account_name_missing(
    client,
    account_id,
    account_type,
    account_name,
    account_balance,
    username,
    expected_status_code,
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
    assert res.status_code == expected_status_code
    assert res.json["account"]["account_name"] == "Squirtle is lucky"


@pytest.mark.parametrize(
    "account_id, account_type, account_balance, username, expected_status_code",
    [
        ("", 1, None, "johnsmith", 200),
    ],
)
def test_account_balance_missing_on_creation(
    client, account_id, account_type, account_balance, username, expected_status_code
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
    assert res.status_code == expected_status_code
    assert res.json["account"]["account_balance"] == 0
