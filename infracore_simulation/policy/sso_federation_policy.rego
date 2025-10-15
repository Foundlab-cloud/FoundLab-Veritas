package foundlab.sso

# By default, all federation attempts are denied.
default allow = false

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

# Allow only if no deny rules are triggered AND there is explicit consent from the resource owner.
allow {
  input.action == "federation_bind"
  count(deny) == 0
  input.explicit_consent == true
}
