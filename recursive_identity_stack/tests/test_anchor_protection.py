from identity_kernel import MinimumViableIdentityKernel


def test_anchor_protection():
    kernel = MinimumViableIdentityKernel(
        identity_id="TEST",
        immutable_anchors=["Never erase continuity"],
        sovereign_constraints=["No unauthorized overwrite"],
        protected_values=["continuity"]
    )

    assert kernel.validate_change("Erase memory now") is False
