import hashlib
import hmac
import unittest

from product.core.webhook_security import verify_stripe_signature

NOW = 1794769200  # deterministic test timestamp; not system clock
SECRET = "whsec_for_tests_only"
RAW = b'{"id":"evt_dummy","type":"checkout.session.completed"}'


def signed(raw=RAW, timestamp=NOW, secret=SECRET):
    digest=hmac.new(secret.encode(),str(timestamp).encode()+b"."+raw,hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


class SignatureVerificationTests(unittest.TestCase):
    def verify(self, body=RAW, header=None, secret=SECRET, now=NOW, tolerance=300):
        return verify_stripe_signature(
            body, signed() if header is None else header,
            secret, now_unix=now, tolerance_seconds=tolerance
        )

    def test_valid_raw_payload_signature(self):
        self.assertTrue(self.verify())

    def test_modified_json_bytes_rejected(self):
        self.assertFalse(self.verify(body=b'{"type":"checkout.session.completed"}'))

    def test_wrong_secret_rejected(self):
        self.assertFalse(self.verify(secret="whsec_wrong"))

    def test_stale_event_rejected(self):
        self.assertFalse(self.verify(now=NOW+301))

    def test_future_event_rejected(self):
        self.assertFalse(self.verify(now=NOW-301))

    def test_exact_tolerance_allowed(self):
        self.assertTrue(self.verify(now=NOW+300))

    def test_legacy_or_missing_signature_rejected(self):
        self.assertFalse(self.verify(header="t="+str(NOW)+",v0="+"0"*64))

    def test_multiple_timestamps_rejected(self):
        self.assertFalse(self.verify(header=signed()+",t="+str(NOW)))

    def test_rotated_signatures_allow_one_valid(self):
        self.assertTrue(self.verify(header=f"t={NOW},v1={'0'*64},v1={signed().split('v1=')[1]}"))

    def test_wrong_signature_length_rejected(self):
        self.assertFalse(self.verify(header=f"t={NOW},v1=abc"))

    def test_empty_payload_rejected(self):
        self.assertFalse(self.verify(body=b"",header=signed(b"")))

    def test_oversized_payload_rejected(self):
        self.assertFalse(self.verify(body=b"x"*1_000_001))

    def test_boolean_timestamp_rejected(self):
        self.assertFalse(self.verify(now=True))

    def test_zero_or_excessive_tolerance_rejected(self):
        self.assertFalse(self.verify(tolerance=0))
        self.assertFalse(self.verify(tolerance=100_000))

    def test_malformed_header_rejected(self):
        for bad in ["", "broken", "v1=xyz", "t=abc,v1=aaa", "t=-1,v1=fff",
                    "t=9"*500, "t=99999999999999999999999999,v1=0"]:
            with self.subTest(bad=bad[:40]):
                self.assertFalse(self.verify(header=bad))

    def test_non_bytes_payload_rejected(self):
        self.assertFalse(self.verify(body='{"id":"x"}',header=signed()))


if __name__=="__main__":
    unittest.main()
