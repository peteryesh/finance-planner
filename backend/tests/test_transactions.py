import pytest

TEST_TRANSACTION_DATA = [
    ("", "transaction 1", "2021-12-29", 500, 7, "bought some food", "", "johnsmith"),
    (None, "transaction 2", "2008-03-13", 3766.89, 10, "", None, "janesmith"),
]

TEST_EXISTING_TRANSACTION_DATA = [
    (
        "a58273f4-ed75-419d-b4c6-ecd38d0571c6",
        "transaction 1",
        "2021-12-29",
        500.00,
        7,
        "bought some food",
        "",
        "johnsmith",
    ),
    (
        "070bf38e-65ba-477a-87ca-711bfd0d7fd2",
        "transaction 2",
        "2008-03-13",
        3766.89,
        10,
        "no notes",
        None,
        "janesmith",
    ),
]


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_create_transaction_without_account(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 201
    assert len(res.json["data"]["transaction_id"]) == 36
    assert res.json["data"]["name"] == name
    assert res.json["data"]["date"] == date
    assert res.json["data"]["amount"] == amount
    assert res.json["data"]["category"] == category
    assert res.json["data"]["notes"] == notes
    assert res.json["data"]["account_id"] == account_id
    assert res.json["data"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_create_transaction_with_account(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": 1,
            "account_name": "",
            "account_balance": 0,
            "username": username,
        },
    )
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": post_res.json["data"]["account_id"],
            "username": username,
        },
    )
    assert res.status_code == 201
    assert len(res.json["data"]["transaction_id"]) == 36
    assert res.json["data"]["name"] == name
    assert res.json["data"]["date"] == date
    assert res.json["data"]["amount"] == amount
    assert res.json["data"]["category"] == category
    assert res.json["data"]["notes"] == notes
    assert res.json["data"]["account_id"] == post_res.json["data"]["account_id"]
    assert res.json["data"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    [
        (
            "",
            "jane transaction",
            "2018-11-21",
            200.26,
            5,
            "no notes",
            None,
            "janesmith",
        ),
        (None, "none", "2008-03-13", 3766.89, 10, "some notes", None, ""),
        (None, "transaction", "2008-03-13", 3766.89, 10, "some notes", None, None),
    ],
)
def test_username_invalid(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 400


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_EXISTING_TRANSACTION_DATA,
)
def test_transaction_id_invalid(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 404


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_account_id_not_exists(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": "a58273f4-ed75-419d-b4c6-ecd38d0571c6",
            "username": username,
        },
    )
    assert res.status_code == 404


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    [
        (None, "", "0000-01-01", 0, 1, "some notes", None, "janesmith"),
        (None, "", "10000-01-00", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-00-01", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-13-01", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-001-01", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-01-00", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-01-32", 0, 1, "some notes", None, "janesmith"),
        (None, "", "2000-01-001", 0, 1, "some notes", None, "janesmith"),
    ],
)
def test_date_invalid(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 422


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    [
        (None, "transaction name", "2000-01-01", 0, 0, "some notes", None, "janesmith"),
        (
            None,
            "transaction name",
            "2000-01-01",
            0,
            16,
            "some notes",
            None,
            "janesmith",
        ),
    ],
)
def test_category_invalid(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 400


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    [
        (
            None,
            "transaction name",
            "2000-01-01",
            0,
            0,
            "0woUjXFTtNVivqgZAX97cAY2ujfG8B7Dr2bS5F5QEFu2vv2wkjkmJAdXzIDEbwfYryTmub3TFLA4R3KNTiug1sq9rEsZKNvgVtvSlxSlyhiFo30ktBJuLqVQfCoTPnGymotjD7d0N19TTcMAl4UjjPGHUcfynYAks0XGuDgq5DVQTeUV6tMosWsDF7mtG56E2IHM6Vh5o",
            None,
            "janesmith",
        )
    ],
)
def test_category_invalid(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 400


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_change_transaction_info(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": 1,
            "account_name": "",
            "account_balance": 0,
            "username": username,
        },
    )
    init_res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    new_date = "0001-01-01"
    res = client.post(
        "/transaction",
        json={
            "transaction_id": init_res.json["data"]["transaction_id"],
            "name": name + " plus some added text",
            "date": new_date,
            "amount": amount + 5000,
            "category": category + 2,
            "notes": notes + " and some extra notes",
            "account_id": post_res.json["data"]["account_id"],
            "username": username,
        },
    )
    assert res.status_code == 200
    assert len(res.json["data"]["transaction_id"]) == 36
    assert res.json["data"]["name"] == name + " plus some added text"
    assert res.json["data"]["date"] == new_date
    assert res.json["data"]["amount"] == amount + 5000
    assert res.json["data"]["category"] == category + 2
    assert res.json["data"]["notes"] == notes + " and some extra notes"
    assert res.json["data"]["account_id"] == post_res.json["data"]["account_id"]
    assert res.json["data"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_get_transaction_success(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    trans_id = post_res.json["data"]["transaction_id"]

    res = client.get(f"/transaction?transaction_id={trans_id}&username={username}")

    assert res.status_code == 200
    assert len(res.json["data"]["transaction_id"]) == 36
    assert res.json["data"]["transaction_id"] == trans_id
    assert res.json["data"]["name"] == name
    assert res.json["data"]["date"] == date
    assert res.json["data"]["amount"] == amount
    assert res.json["data"]["category"] == category
    assert res.json["data"]["notes"] == notes
    assert res.json["data"]["account_id"] == account_id
    assert res.json["data"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_EXISTING_TRANSACTION_DATA,
)
def test_get_transaction_failure(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.get(
        f"/transaction?transaction_id={transaction_id}&username={username}"
    )
    assert res.status_code == 404


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_get_all_user_transactions(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    trans_ct = 3
    for i in range(trans_ct):
        client.post(
            "/transaction",
            json={
                "transaction_id": transaction_id,
                "name": name,
                "date": date,
                "amount": amount,
                "category": category,
                "notes": notes,
                "account_id": account_id,
                "username": username,
            },
        )
    res = client.get(f"/transaction?username={username}")
    assert res.status_code == 200
    assert len(res.json["data"]) == trans_ct


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_get_all_user_transactions_with_account(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    acct_res = client.post(
        "/account",
        json={
            "account_id": account_id,
            "account_type": 1,
            "account_name": "",
            "account_balance": 0,
            "username": username,
        },
    )
    acct_id = acct_res.json["data"]["account_id"]
    trans_ct = 5
    for i in range(trans_ct):
        client.post(
            "/transaction",
            json={
                "transaction_id": transaction_id,
                "name": name,
                "date": date,
                "amount": amount,
                "category": category,
                "notes": notes,
                "account_id": acct_id,
                "username": username,
            },
        )
    res = client.get(f"/transaction?username={username}&account_id={acct_id}")
    assert res.status_code == 200
    assert len(res.json["data"]) == trans_ct


@pytest.mark.parametrize(
    "username, account_id",
    {
        ("johnsmith", "1fb49b3d-6078-4671-92f7-1cb16710f6ce"),
        ("janesmith", "01901f87-6c64-4d37-a0c3-7590797f609a"),
    },
)
def test_get_all_user_transactions_not_found(client, username, account_id):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.get(f"/transaction?username={username}&account_id={account_id}")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_delete_transaction_exists(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    post_res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "name": name,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    trans_id = post_res.json["data"]["transaction_id"]

    res = client.delete(f"/transaction?transaction_id={trans_id}&username={username}")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "transaction_id, name, date, amount, category, notes, account_id, username",
    TEST_EXISTING_TRANSACTION_DATA,
)
def test_delete_transaction_not_exists(
    client, transaction_id, name, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.delete(
        f"/transaction?transaction_id={transaction_id}&username={username}"
    )
    assert res.status_code == 204
