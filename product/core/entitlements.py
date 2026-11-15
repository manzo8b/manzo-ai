"""MANZO AI SaaS foundations: pure, fail-closed entitlement policy.

This module is a TESTABLE REFERENCE IMPLEMENTATION, NOT a live authorization
server or billing integration. In production, caller identity, organization,
grants and consumption MUST be loaded server-side from authenticated, audited
records. Never accept entitlement values directly from a browser.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

class DecisionCode(str, Enum):
    ALLOW = "allow"
    INVALID = "invalid_input"
    TENANT_MISMATCH = "tenant_mismatch"
    NO_GRANT = "no_grant"
    NOT_ACTIVE = "not_active"
    EXPIRED = "expired"
    QUOTA_EXHAUSTED = "quota_exhausted"

@dataclass(frozen=True)
class Principal:
    """Server-verified identity and organization; never a user-submitted claim."""
    user_id: str
    organization_id: str

@dataclass(frozen=True)
class Grant:
    """Backend record created only after approved provisioning or verified billing."""
    organization_id: str
    feature: str
    status: str
    expires_at: datetime
    usage_limit: int

@dataclass(frozen=True)
class Usage:
    organization_id: str
    feature: str
    consumed: int

@dataclass(frozen=True)
class Decision:
    allowed: bool
    code: DecisionCode

def authorize_feature(
    principal: Principal | None,
    grant: Grant | None,
    usage: Usage | None,
    *,
    requested_feature: str,
    now: datetime,
) -> Decision:
    """Conservative reference rule; usage decrement must be atomic in real backend.

    This does not prove user session authenticity, organization membership,
    Stripe webhook validity or concurrent-safe quota accounting.
    """
    deny = lambda code: Decision(False, code)
    if not isinstance(principal, Principal) or not isinstance(now, datetime):
        return deny(DecisionCode.INVALID)
    if now.tzinfo is None or now.utcoffset() is None:
        return deny(DecisionCode.INVALID)
    if not all(
        isinstance(s, str) and s.strip()
        for s in (principal.user_id, principal.organization_id, requested_feature)
    ):
        return deny(DecisionCode.INVALID)
    if grant is None or usage is None:
        return deny(DecisionCode.NO_GRANT)
    if not isinstance(grant, Grant) or not isinstance(usage, Usage):
        return deny(DecisionCode.INVALID)
    if grant.organization_id != principal.organization_id or usage.organization_id != principal.organization_id:
        return deny(DecisionCode.TENANT_MISMATCH)
    if grant.feature != requested_feature or usage.feature != requested_feature:
        return deny(DecisionCode.NO_GRANT)
    if grant.status != "active":
        return deny(DecisionCode.NOT_ACTIVE)
    if not isinstance(grant.expires_at, datetime):
        return deny(DecisionCode.INVALID)
    if grant.expires_at.tzinfo is None or grant.expires_at.utcoffset() is None:
        return deny(DecisionCode.INVALID)
    if now.astimezone(timezone.utc) >= grant.expires_at.astimezone(timezone.utc):
        return deny(DecisionCode.EXPIRED)
    if type(grant.usage_limit) is not int or type(usage.consumed) is not int:
        return deny(DecisionCode.INVALID)
    if grant.usage_limit < 0 or usage.consumed < 0:
        return deny(DecisionCode.INVALID)
    if usage.consumed >= grant.usage_limit:
        return deny(DecisionCode.QUOTA_EXHAUSTED)
    return Decision(True, DecisionCode.ALLOW)
