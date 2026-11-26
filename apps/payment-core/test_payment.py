import os
from concurrent.futures import ThreadPoolExecutor
import pytest
from fastapi.testclient import TestClient

os.environ["PAYMENT_API_KEY"] = "test-secure-eu-key-999"
os.environ["SERVER_REGION"] = "eu-north-1"
os.environ["DB_PATH"] = ":memory:"

import main  # noqa: E402

client = TestClient(main.app)
VALID_PAYLOAD = {
    "sender_iban": "DE89370400440532013000",
    "receiver_iban": "NL91ABNA0417164300",
    "amount_eur": "250.75",
}


@pytest.fixture(autouse=True)
def clean_state(monkeypatch):
    """Reset region and database table before every test."""
    monkeypatch.setattr(main, "ALLOWED_SERVER_REGION", "eu-north-1")
    main.init_db()
    with main.get_db_connection() as conn:
        conn.execute("DELETE FROM transactions")
        conn.commit()
    yield


def test_1_valid_payment():
    res = client.post(
        "/api/v1/pay",
        headers={"x-api-key": "test-secure-eu-key-999", "idempotency-key": "idem-valid-001"},
        json=VALID_PAYLOAD,
    )
    assert res.status_code == 200
    body = res.json()
    assert body["transaction"]["status"] == "COMPLETED"
    assert body["transaction"]["amount_eur"] == "250.75"


def test_2_invalid_api_key_rejected():
    res = client.post(
        "/api/v1/pay",
        headers={"x-api-key": "invalid-secret", "idempotency-key": "idem-auth-002"},
        json=VALID_PAYLOAD,
    )
    assert res.status_code == 401


def test_3_invalid_iban_checksum_rejected():
    bad_payload = {**VALID_PAYLOAD, "sender_iban": "DE89370400440532013099"}
    res = client.post(
        "/api/v1/pay",
        headers={"x-api-key": "test-secure-eu-key-999", "idempotency-key": "idem-iban-003"},
        json=bad_payload,
    )
    assert res.status_code == 422


def test_4_zero_and_negative_amount_rejected():
    for idx, amt in enumerate(["0.00", "-10.00"]):
        res = client.post(
            "/api/v1/pay",
            headers={"x-api-key": "test-secure-eu-key-999", "idempotency-key": f"idem-zero-{idx}-004"},
            json={**VALID_PAYLOAD, "amount_eur": amt},
        )
        assert res.status_code == 422


def test_5_excessive_amount_rejected():
    res = client.post(
        "/api/v1/pay",
        headers={"x-api-key": "test-secure-eu-key-999", "idempotency-key": "idem-limit-005"},
        json={**VALID_PAYLOAD, "amount_eur": "10000.01"},
    )
    assert res.status_code == 422


def test_6_same_idempotency_key_returns_same_transaction():
    headers = {"x-api-key": "test-secure-eu-key-999", "idempotency-key": "idem-replay-006"}
    res1 = client.post("/api/v1/pay", headers=headers, json=VALID_PAYLOAD)
    res2 = client.post("/api/v1/pay", headers=headers, json=VALID_PAYLOAD)
    assert res1.status_code == 200
    assert res2.status_code == 200
    assert res1.json()["transaction"]["tx_id"] == res2.json()["transaction"]["tx_id"]


def test_7_non_eu_and_spoofed_eu_region_rejected(monkeypatch):
    for bad_region in ["us-east-1", "eu-evil", "eu-test"]:
        monkeypatch.setattr(main, "ALLOWED_SERVER_REGION", bad_region)
        res = client.post(
            "/api/v1/pay",
            headers={"x-api-key": "test-secure-eu-key-999", "idempotency-key": f"idem-reg-{bad_region}"},
            json=VALID_PAYLOAD,
        )
        assert res.status_code == 403


def test_8_concurrent_same_idempotency_requests():
    headers = {"x-api-key": "test-secure-eu-key-999", "idempotency-key": "idem-concurrent-008"}

    def send_request():
        return client.post("/api/v1/pay", headers=headers, json=VALID_PAYLOAD)

    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(lambda _: send_request(), range(5)))

    assert all(r.status_code == 200 for r in responses)
    tx_ids = {r.json()["transaction"]["tx_id"] for r in responses}
    assert len(tx_ids) == 1


def test_9_health_works_without_api_key():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"
    assert "server_region" not in res.json()
