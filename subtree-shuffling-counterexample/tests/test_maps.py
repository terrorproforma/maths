from shuffle_counterexample.maps import verify_three_variable_maps


def test_three_variable_map_certificate() -> None:
    report = verify_three_variable_maps()
    assert report["original_jacobian"] == "-2"
    assert report["normalized_jacobian"] == "1"
    assert report["original_collision_count"] == 3
    assert report["normalized_collision_count"] == 3
