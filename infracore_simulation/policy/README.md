# Veritas Policy-as-Code

This directory contains the security policy, written in Rego, that governs the SSO federation process in our simulation.

## `sso_federation_policy.rego`

This file is the technical implementation of our Zero-Trust philosophy. Let's break down its core logic:

### 1. Default Deny

```rego
# By default, all federation attempts are denied.
default allow = false
```
This is the most critical rule. It establishes a "guilty until proven innocent" posture. Unless a request meets a strict set of criteria to be explicitly allowed, it will be rejected. This prevents unforeseen vulnerabilities and ensures that only known, trusted interactions can occur.

### 2. Denial Logic

The policy defines specific conditions under which a request **must** be denied.

```rego
# Deny if there is no verified relationship with the initiating organization.
deny[msg] {
  input.action == "federation_bind"
  not input.initiator.has_verified_relationship
  msg := "REL_001_NO_VERIFIED_RELATIONSHIP"
}

# Deny if there is no active contract with the initiating organization.
deny[msg] {
  input.action == "federation_bind"
  not input.initiator.has_active_contract
  msg := "POL_403_HARD_DENY_IF_NO_CONTRACT"
}
```
In the context of the NVIDIA incident, the request from 'Accenture' would have failed both of these checks, as there was no verified relationship or active contract.

### 3. Explicit Allow Condition

Finally, the policy defines the *only* scenario in which a federation is permitted.

```rego
# Allow only if no deny rules are triggered AND there is explicit consent from the resource owner.
allow {
  input.action == "federation_bind"
  count(deny) == 0
  input.explicit_consent == true
}
```
This rule mandates that two conditions must be met simultaneously:
1.  No `deny` rules were triggered.
2.  The request payload contains proof of `explicit_consent` from the resource owner (in this case, FoundLab).

This policy makes the security posture of the system explicit, auditable, and deterministic. It is the executable form of trust.
