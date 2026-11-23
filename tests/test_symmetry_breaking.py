"""Unit tests for Circuit-Level Automorphism Subgroup & Symmetry Breaking."""

import pytest
from orbit_tied_qnbp.experiments.analyze_dem_symmetry_breaking import analyze_symmetry_subgroups


def test_symmetry_breaking_maximal_subgroup():
    """Verify that torus translation Z_l x Z_m is the maximal exact symmetry subgroup."""
    res = analyze_symmetry_subgroups(num_rounds=3, physical_p=0.003)

    # Torus translations must be exact automorphisms
    assert res["torus_translations_Zl_Zm"]["preserved"] is True
    assert res["torus_translations_Zl_Zm"]["violations"] == 0

    # Spatial inversion is broken by directed CNOT schedule
    assert res["spatial_inversion"]["preserved"] is False
    assert res["spatial_inversion"]["violations"] > 0

    # Temporal translation is broken by window boundaries
    assert res["temporal_translation"]["preserved"] is False
    assert res["temporal_translation"]["classes"] == 3

    # CSS duality is broken
    assert res["css_duality"]["preserved"] is False

    assert res["maximal_exact_subgroup"] == "Z_l x Z_m"
