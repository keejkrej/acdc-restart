"""Crossfade math for brightfield, fluorescence, and segmentation layers."""

from __future__ import annotations


def crossfade_opacities(value_0_to_100: float) -> tuple[float, float]:
    """Return ``(first, second)`` opacities for a 0–100 crossfade slider."""
    t = max(0.0, min(100.0, float(value_0_to_100))) / 100.0
    return 1.0 - t, t


def layer_opacities(
    bf_fluor_blend_0_to_100: float,
    image_seg_blend_0_to_100: float,
    *,
    has_fluorescence: bool,
) -> tuple[float, float, float]:
    """Return ``(bf_opacity, fluo_opacity, seg_opacity)`` for display layers."""
    if has_fluorescence:
        bf_w, fluo_w = crossfade_opacities(bf_fluor_blend_0_to_100)
    else:
        bf_w, fluo_w = 1.0, 0.0
    image_scale, seg_scale = crossfade_opacities(image_seg_blend_0_to_100)
    return bf_w * image_scale, fluo_w * image_scale, seg_scale
