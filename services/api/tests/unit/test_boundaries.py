from flowverse_api.modules import BOUNDARIES


def test_api_owns_eight_non_business_module_boundaries() -> None:
    names = {boundary.name for boundary in BOUNDARIES}

    assert names == {
        "identity_access",
        "task_lifecycle",
        "creative_reference",
        "creative_content",
        "review_compliance",
        "release_cycle",
        "feedback_decision",
        "governance_ops",
    }
    assert all(boundary.public_contracts == () for boundary in BOUNDARIES)
    assert all(boundary.owns_data == () for boundary in BOUNDARIES)
    assert all(boundary.depends_on == () for boundary in BOUNDARIES)
