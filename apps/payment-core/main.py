import os
import re
import sqlite3
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator


# ============================================================
# Security Configuration
# ============================================================

EXPECTED_API_KEY = os.getenv("PAYMENT_API_KEY")

if not EXPECTED_API_KEY:
    raise RuntimeError(
        "CRITICAL SECURITY ERROR: PAYMENT_API_KEY environment variable is required!"
    )

ALLOWED_SERVER_REGION = os.getenv("SERVER_REGION", "eu-north-1")
DB_PATH = os.getenv("DB_PATH", "transactions.db")

ALLOWED_EU_REGIONS = {
    "eu-north-1",
    "eu-west-1",
    "eu-central-1",
    "eu-south-1",
}


# ============================================================
# Application
# ============================================================

app = FastAPI(
    title="Security-Focused Payment Core",
    description=(
        "DevSecOps evidence prototype with API-key authentication, "
        "IBAN Mod-97 validation, EU region enforcement, "
        "and idempotent transaction handling."
    ),
    version="3.2.2",
)


# ============================================================
# Database
# ============================================================

_SHARED_MEMORY_URI = "file:payment_core_memdb?mode=memory&cache=shared"
_memory_keepalive: sqlite3.Connection | None = None


def get_db_connection() -> sqlite3.Connection:
    """
    Create a SQLite connection.

    For tests using DB_PATH=:memory:, a shared in-memory database
    is kept alive so the schema survives across connections.
    """
    global _memory_keepalive

    if DB_PATH == ":memory:":
        if _memory_keepalive is None:
            _memory_keepalive = sqlite3.connect(
                _SHARED_MEMORY_URI,
                uri=True,
                timeout=10.0,
                check_same_thread=False,
            )

        return sqlite3.connect(
            _SHARED_MEMORY_URI,
            uri=True,
            timeout=10.0,
            check_same_thread=False,
        )

    return sqlite3.connect(
        DB_PATH,
        timeout=10.0,
        check_same_thread=False,
    )


def init_db() -> None:
    """Create the transaction table if it does not already exist."""
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                idempotency_key TEXT PRIMARY KEY,
                tx_id TEXT NOT NULL,
                sender_iban TEXT NOT NULL,
                receiver_iban TEXT NOT NULL,
                amount_eur TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


init_db()


# ============================================================
# Authentication
# ============================================================

def verify_api_key(x_api_key: str = Header(...)) -> None:
    """Authenticate requests using the X-API-Key header."""
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid API Key",
        )


# ============================================================
# IBAN Validation
# ============================================================

def is_valid_iban_checksum(iban: str) -> bool:
    """
    Validate an IBAN using ISO-13616 Mod-97.

    IBAN algorithm:
    1. Move first four characters to the end.
    2. Convert letters to numbers (A=10 ... Z=35).
    3. Verify remainder equals 1.
    """
    rearranged = iban[4:] + iban[:4]

    numeric_iban = "".join(
        str(int(character, 36))
        for character in rearranged
    )

    return int(numeric_iban) % 97 == 1


class PaymentRequest(BaseModel):
    sender_iban: str
    receiver_iban: str
    amount_eur: Decimal = Field(
        gt=Decimal("0.00"),
        le=Decimal("10000.00"),
        decimal_places=2,
    )

    @field_validator("sender_iban", "receiver_iban")
    @classmethod
    def validate_iban(cls, value: str) -> str:
        cleaned = value.replace(" ", "").upper()

        if not re.fullmatch(
            r"[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}",
            cleaned,
        ):
            raise ValueError("Invalid IBAN structural format")

        if not is_valid_iban_checksum(cleaned):
            raise ValueError(
                "Invalid IBAN checksum "
                "(ISO-13616 Mod-97 verification failed)"
            )

        return cleaned


# ============================================================
# Transaction Helpers
# ============================================================

def fetch_existing_tx(
    cursor: sqlite3.Cursor,
    idempotency_key: str,
) -> dict | None:
    """Return an existing transaction for an idempotency key."""
    cursor.execute(
        """
        SELECT
            tx_id,
            sender_iban,
            receiver_iban,
            amount_eur,
            status,
            created_at
        FROM transactions
        WHERE idempotency_key = ?
        """,
        (idempotency_key,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "tx_id": row[0],
        "sender_iban": row[1],
        "receiver_iban": row[2],
        "amount_eur": row[3],
        "status": row[4],
        "created_at": row[5],
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health_check() -> dict:
    """Minimal liveness endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# Payment Endpoint
# ============================================================

@app.post(
    "/api/v1/pay",
    dependencies=[Depends(verify_api_key)],
)
def process_payment(
    payment: PaymentRequest,
    idempotency_key: str = Header(
        ...,
        min_length=8,
        max_length=64,
        pattern=r"^[a-zA-Z0-9_-]+$",
    ),
) -> dict:
    """
    Process a payment with:
    - API-key authentication
    - EU region enforcement
    - validated IBANs
    - bounded payment amount
    - persistent idempotency
    """

    # --------------------------------------------------------
    # EU Data Residency Enforcement
    # --------------------------------------------------------

    if ALLOWED_SERVER_REGION not in ALLOWED_EU_REGIONS:
        raise HTTPException(
            status_code=403,
            detail=(
                "Data Residency Policy: Server must operate "
                "within an approved EU region"
            ),
        )

    tx_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    # --------------------------------------------------------
    # Transaction Storage
    # --------------------------------------------------------

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check for an existing idempotency key.
        existing = fetch_existing_tx(
            cursor,
            idempotency_key,
        )

        if existing:
            return {
                "message": "Idempotent replay: Transaction already processed",
                "transaction": existing,
            }

        try:
            cursor.execute(
                """
                INSERT INTO transactions (
                    idempotency_key,
                    tx_id,
                    sender_iban,
                    receiver_iban,
                    amount_eur,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    idempotency_key,
                    tx_id,
                    payment.sender_iban,
                    payment.receiver_iban,
                    str(payment.amount_eur),
                    "COMPLETED",
                    created_at,
                ),
            )

            conn.commit()

        except sqlite3.IntegrityError:
            # Another concurrent request may have inserted
            # the same idempotency key first.
            existing = fetch_existing_tx(
                cursor,
                idempotency_key,
            )

            if existing:
                return {
                    "message": (
                        "Idempotent replay: "
                        "Concurrent collision handled safely"
                    ),
                    "transaction": existing,
                }

            raise

    # --------------------------------------------------------
    # Successful Payment Response
    # --------------------------------------------------------

    return {
        "message": "Payment processed securely",
        "transaction": {
            "tx_id": tx_id,
            "sender_iban": payment.sender_iban,
            "receiver_iban": payment.receiver_iban,
            "amount_eur": str(payment.amount_eur),
            "status": "COMPLETED",
            "created_at": created_at,
        },
  }
