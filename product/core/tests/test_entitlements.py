import unittest
from datetime import datetime, timedelta, timezone

from product.core.entitlements import (
    Principal, Grant, Usage, DecisionCode, authorize_feature
)

NOW=datetime(2026,11,15,tzinfo=timezone.utc)

class EntitlementsTest(unittest.TestCase):
    def setUp(self):
        self.user=Principal("user-1","org-a")
        self.grant=Grant("org-a","studio.generate","active",NOW+timedelta(days=30),10)
        self.usage=Usage("org-a","studio.generate",3)
    def check(self,code,principal=None,grant=None,usage=None,feature="studio.generate",when=NOW):
        result=authorize_feature(
            self.user if principal is None else principal,
            self.grant if grant is None else grant,
            self.usage if usage is None else usage,
            requested_feature=feature,now=when
        )
        self.assertEqual(result.code,code)
        self.assertEqual(result.allowed,code is DecisionCode.ALLOW)

    def test_valid_grant(self):
        self.check(DecisionCode.ALLOW)
    def test_other_organization_cannot_use_grant(self):
        self.check(DecisionCode.TENANT_MISMATCH,
                   principal=Principal("user-2","org-b"))
    def test_usage_is_also_tenant_bound(self):
        self.check(DecisionCode.TENANT_MISMATCH,
                   usage=Usage("org-b","studio.generate",0))
    def test_wrong_feature(self):
        self.check(DecisionCode.NO_GRANT,feature="verify.process")
    def test_expired_is_denied_at_boundary(self):
        self.check(DecisionCode.EXPIRED,when=self.grant.expires_at)
    def test_suspended_account_denied(self):
        g=Grant("org-a","studio.generate","suspended",self.grant.expires_at,10)
        self.check(DecisionCode.NOT_ACTIVE,grant=g)
    def test_exhausted_quota(self):
        self.check(DecisionCode.QUOTA_EXHAUSTED,usage=Usage("org-a","studio.generate",10))
    def test_negative_usage_does_not_grant_access(self):
        self.check(DecisionCode.INVALID,usage=Usage("org-a","studio.generate",-1))
    def test_boolean_usage_cannot_be_used_as_integer(self):
        self.check(DecisionCode.INVALID,usage=Usage("org-a","studio.generate",True))
    def test_naive_datetime_rejected(self):
        result=authorize_feature(self.user,self.grant,self.usage,
           requested_feature="studio.generate",now=datetime(2026,11,15))
        self.assertEqual(result.code,DecisionCode.INVALID)
    def test_missing_grant_denied(self):
        result=authorize_feature(self.user,None,self.usage,requested_feature="studio.generate",now=NOW)
        self.assertEqual(result.code,DecisionCode.NO_GRANT)
    def test_no_identity_denied(self):
        result=authorize_feature(None,self.grant,self.usage,requested_feature="studio.generate",now=NOW)
        self.assertEqual(result.code,DecisionCode.INVALID)
    def test_invalid_identity_denied(self):
        result=authorize_feature(Principal("","org-a"),self.grant,self.usage,
           requested_feature="studio.generate",now=NOW)
        self.assertEqual(result.code,DecisionCode.INVALID)
    def test_backend_counter_is_not_changed(self):
        result=authorize_feature(self.user,self.grant,self.usage,requested_feature="studio.generate",now=NOW)
        self.assertTrue(result.allowed)
        self.assertEqual(self.usage.consumed,3) # real backend needs atomic database debit

if __name__=="__main__":
    unittest.main()
