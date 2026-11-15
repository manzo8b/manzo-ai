"""Pure signature verification contract for a FUTURE Stripe webhook endpoint.

Not a webhook receiver: this does not deserialize events, contact Stripe,
create subscriptions, or grant access. Production endpoint must also:
- read the exact raw HTTP request body (not reserialized JSON)
- load secret from server-side secret manager
- verify signing key rotation and event authenticity/ownership
- atomically record (provider, event_id) before idempotent processing
- reconcile payment statuses through provider APIs when necessary.
"""
from __future__ import annotations

import hashlib
import hmac
import re

_MAX_BODY_BYTES = 1_000_000
_MAX_HEADER_CHARS = 2048
_SIGNATURE_HEX = re.compile(r"^[0-9a-fA-F]{64}$")


def verify_stripe_signature(
    raw_body: bytes,
    signature_header: str,
    signing_secret: str,
    *,
    now_unix: int,
    tolerance_seconds: int = 300,
) -> bool:
    """Return False on missing, malformed, stale, future or invalid signatures.

    Implements Stripe's documented HMAC-SHA256 signed-payload format.
    The function is deliberately independent of any payment-account connection.
    """
    if not isinstance(raw_body, bytes) or not 0 < len(raw_body) <= _MAX_BODY_BYTES:
        return False
    if not isinstance(signature_header, str) or not 0 < len(signature_header) <= _MAX_HEADER_CHARS:
        return False
    if not isinstance(signing_secret, str) or not signing_secret.strip():
        return False
    if type(now_unix) is not int or now_unix < 0:
        return False
    if type(tolerance_seconds) is not int or not 1 <= tolerance_seconds <= 300:
        return False

    entries = [part.strip().split("=", 1) for part in signature_header.split(",")]
    if any(len(item) != 2 for item in entries):
        return False
    timestamps = [value for key, value in entries if key == "t"]
    versions = [value for key, value in entries if key == "v1"]

    if len(timestamps) != 1 or not timestamps[0].isdigit() or len(timestamps[0]) > 15:
        return False
    if not versions or len(versions) > 8:
        return False

    timestamp = int(timestamps[0])
    if abs(now_unix - timestamp) > tolerance_seconds:
        return False

    data = str(timestamp).encode("ascii") + b"." + raw_body
    expected = hmac.new(signing_secret.encode("utf-8"), data, hashlib.sha256).hexdigest()

    return any(
        bool(_SIGNATURE_HEX.fullmatch(signature))
        and hmac.compare_digest(expected, signature.lower())
        for signature in versions
    )
