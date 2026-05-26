"""Tests for crossfade layer opacity math."""

from __future__ import annotations

from cellacdc.blend import crossfade_opacities, layer_opacities


def test_crossfade_opacities_endpoints() -> None:
    assert crossfade_opacities(0) == (1.0, 0.0)
    assert crossfade_opacities(100) == (0.0, 1.0)
    assert crossfade_opacities(50) == (0.5, 0.5)


def test_layer_opacities_without_fluorescence() -> None:
    bf, fluo, seg = layer_opacities(50, 0, has_fluorescence=False)
    assert fluo == 0.0
    assert bf == 1.0
    assert seg == 0.0

    bf, fluo, seg = layer_opacities(50, 100, has_fluorescence=False)
    assert bf == 0.0
    assert fluo == 0.0
    assert seg == 1.0


def test_layer_opacities_with_fluorescence() -> None:
    bf, fluo, seg = layer_opacities(0, 0, has_fluorescence=True)
    assert bf == 1.0
    assert fluo == 0.0
    assert seg == 0.0

    bf, fluo, seg = layer_opacities(100, 50, has_fluorescence=True)
    assert bf == 0.0
    assert fluo == 0.5
    assert seg == 0.5
