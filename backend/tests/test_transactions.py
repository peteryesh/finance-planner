import pytest

TEST_TRANSACTION_DATA = [
    ("", "2021-12-29", 500, 7, "bought some food", "", "johnsmith"),
    (None, "2008-03-13", 3766.89, 10, "", None, "janesmith"),
]

TEST_EXISTING_TRANSACTION_DATA = [
    (
        "a58273f4-ed75-419d-b4c6-ecd38d0571c6",
        "2021-12-29",
        500.00,
        7,
        "bought some food",
        "",
        "johnsmith",
    ),
    (
        "070bf38e-65ba-477a-87ca-711bfd0d7fd2",
        "2008-03-13",
        3766.89,
        10,
        "no notes",
        None,
        "janesmith",
    ),
]


@pytest.mark.parametrize(
    "transaction_id, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_create_transaction_without_account(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 201
    assert len(res.json["transaction"]["transaction_id"]) == 36
    assert res.json["transaction"]["date"] == date
    assert res.json["transaction"]["amount"] == amount
    assert res.json["transaction"]["category"] == category
    assert res.json["transaction"]["notes"] == notes
    assert res.json["transaction"]["account_id"] == account_id
    assert res.json["transaction"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_create_transaction_with_account(
    client, transaction_id, date, amount, category, notes, account_id, username
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
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": acct_res.json["account"]["account_id"],
            "username": username,
        },
    )
    assert res.status_code == 201
    assert len(res.json["transaction"]["transaction_id"]) == 36
    assert res.json["transaction"]["date"] == date
    assert res.json["transaction"]["amount"] == amount
    assert res.json["transaction"]["category"] == category
    assert res.json["transaction"]["notes"] == notes
    assert (
        res.json["transaction"]["account_id"] == acct_res.json["account"]["account_id"]
    )
    assert res.json["transaction"]["username"] == username


@pytest.mark.parametrize(
    "transaction_id, date, amount, category, notes, account_id, username",
    [
        ("", "2018-11-21", 200.26, 5, "no notes", None, "janesmith"),
        (None, "2008-03-13", 3766.89, 10, "some notes", None, ""),
        (None, "2008-03-13", 3766.89, 10, "some notes", None, None),
    ],
)
def test_username_invalid(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
    "transaction_id, date, amount, category, notes, account_id, username",
    TEST_EXISTING_TRANSACTION_DATA,
)
def test_transaction_id_invalid(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
    "transaction_id, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_account_id_not_exists(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
    "transaction_id, date, amount, category, notes, account_id, username",
    [
        (None, "0000-01-01", 0, 1, "some notes", None, "janesmith"),
        (None, "10000-01-00", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-00-01", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-13-01", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-001-01", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-01-00", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-01-32", 0, 1, "some notes", None, "janesmith"),
        (None, "2000-01-001", 0, 1, "some notes", None, "janesmith"),
    ],
)
def test_date_invalid(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
            "date": date,
            "amount": amount,
            "category": category,
            "notes": notes,
            "account_id": account_id,
            "username": username,
        },
    )
    assert res.status_code == 422


# @pytest.mark.parametrize()
# def test_amount_type():
#     pass

# @pytest.mark.parametrize()
# def test_amount_values():
#     pass


@pytest.mark.parametrize(
    "transaction_id, date, amount, category, notes, account_id, username",
    [
        (None, "2000-01-01", 0, 0, "some notes", None, "janesmith"),
        (None, "2000-01-01", 0, 16, "some notes", None, "janesmith"),
    ],
)
def test_category_invalid(
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
    "transaction_id, date, amount, category, notes, account_id, username",
    [
        (
            None,
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
    client, transaction_id, date, amount, category, notes, account_id, username
):
    client.post("/user", json={"username": username, "first_name": "", "last_name": ""})
    res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
    "transaction_id, date, amount, category, notes, account_id, username",
    TEST_TRANSACTION_DATA,
)
def test_change_transaction_info(
    client, transaction_id, date, amount, category, notes, account_id, username
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
    init_res = client.post(
        "/transaction",
        json={
            "transaction_id": transaction_id,
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
            "transaction_id": init_res.json["transaction"]["transaction_id"],
            "date": new_date,
            "amount": amount + 5000,
            "category": category + 2,
            "notes": notes + " and some extra notes",
            "account_id": acct_res.json["account"]["account_id"],
            "username": username,
        },
    )
    assert res.status_code == 200
    assert len(res.json["transaction"]["transaction_id"]) == 36
    assert res.json["transaction"]["date"] == new_date
    assert res.json["transaction"]["amount"] == amount + 5000
    assert res.json["transaction"]["category"] == category + 2
    assert res.json["transaction"]["notes"] == notes + " and some extra notes"
    assert (
        res.json["transaction"]["account_id"] == acct_res.json["account"]["account_id"]
    )
    assert res.json["transaction"]["username"] == username
