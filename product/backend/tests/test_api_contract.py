"""Verify the intentionally unimplemented MANZO AI API design contract."""
import json
import re
import unittest
from pathlib import Path

SPEC=Path(__file__).resolve().parents[1]/"contracts"/"openapi.json"


class ApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(SPEC.read_text(encoding="utf-8"))
        cls.paths=cls.doc["paths"]
        cls.schemas=cls.doc["components"]["schemas"]

    def test_explicitly_unimplemented(self):
        self.assertEqual(self.doc["info"]["x-manzo-implementation-status"],"unimplemented-design-contract")
        self.assertNotIn("servers",self.doc)

    def test_every_operation_has_unique_id_and_response(self):
        ids=[]
        for p,methods in self.paths.items():
            self.assertTrue(p.startswith("/v1/"))
            for method,op in methods.items():
                self.assertIn(method,("get","post"))
                ids.append(op["operationId"])
                self.assertIn("responses",op)
                self.assertTrue(op["summary"])
        self.assertEqual(len(ids),len(set(ids)))

    def test_authentication_default_fails_closed(self):
        self.assertEqual(self.doc["security"],[{"BearerAuth":[]}])
        for path,methods in self.paths.items():
            for _,operation in methods.items():
                if path in ("/v1/health","/v1/billing/stripe-webhook"):
                    self.assertEqual(operation["security"],[])
                else:
                    self.assertNotEqual(operation.get("security",self.doc["security"]),[])

    def test_webhook_signature_required_and_raw_body_documented(self):
        endpoint=self.paths["/v1/billing/stripe-webhook"]["post"]
        self.assertIn("Stripe-Signature",[p["name"] for p in endpoint["parameters"]])
        self.assertIn("raw",endpoint["description"].lower())
        self.assertIn("400",endpoint["responses"])

    def test_checkout_has_no_client_price_or_grant_fields(self):
        body=self.schemas["CheckoutRequest"]
        self.assertEqual(set(body["properties"]),{"organizationId","planCode"})
        self.assertFalse(body["additionalProperties"])
        self.assertIn("server",self.paths["/v1/billing/checkout-sessions"]["post"]["description"].lower())

    def test_attempt_scores_are_not_client_submitted(self):
        body=self.schemas["AttemptSubmission"]
        self.assertEqual(set(body["properties"]),{"courseId","versionId","assessmentId","selections"})
        self.assertFalse(body["additionalProperties"])
        self.assertNotIn("score",body["properties"])

    def test_budget_not_user_controlled(self):
        body=self.schemas["AgentRequest"]
        self.assertFalse(body["additionalProperties"])
        forbidden={"budget","price","cost","tokenLimit","apiKey","organizationId"}
        self.assertFalse(set(body["properties"])&forbidden)
        self.assertIn("429",self.paths["/v1/organizations/{organizationId}/agent-runs"]["post"]["responses"])

    def test_internal_references_resolve(self):
        all_refs=[]
        def walk(value):
            if isinstance(value,dict):
                for key,v in value.items():
                    if key=="$ref":all_refs.append(v)
                    walk(v)
            elif isinstance(value,list):
                for x in value:walk(x)
        walk(self.doc)
        self.assertGreater(len(all_refs),10)
        for ref in all_refs:
            self.assertTrue(ref.startswith("#/components/"),ref)
            curr=self.doc
            for segment in ref.lstrip("#/").split("/"):
                self.assertIn(segment,curr)
                curr=curr[segment]

    def test_tenant_path_parameters_declared(self):
        for path,methods in self.paths.items():
            if "{organizationId}" not in path:continue
            for operation in methods.values():
                refs=[p["$ref"] for p in operation.get("parameters",[]) if "$ref" in p]
                self.assertIn("#/components/parameters/OrganizationId",refs)

    def test_no_real_provider_credentials_or_checkout_links(self):
        serialized=json.dumps(self.doc).lower()
        for value in ("sk_live_", "whsec_live_", "pk_live_", "price_1", "checkout.stripe.com/c/pay"):
            self.assertNotIn(value,serialized)


if __name__=="__main__":
    unittest.main()
