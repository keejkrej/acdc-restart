"""Brush/eraser operations and stack dimension helpers."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StackLayout:
    """Normalized view of image/mask dimensionality."""

    ndim: int
    has_time: bool
    has_z: bool
    size_t: int
    size_z: int
    size_y: int
    size_x: int


def infer_layout(shape: tuple[int, ...]) -> StackLayout:
    if len(shape) == 2:
        y, x = shape
        return StackLayout(2, False, False, 1, 1, y, x)
    if len(shape) == 3:
        # Heuristic: if first dim is small (<=64), treat as Z; else T
        d0, y, x = shape
        if d0 <= 64:
            return StackLayout(3, False, True, 1, d0, y, x)
        return StackLayout(3, True, False, d0, 1, y, x)
    if len(shape) == 4:
        t, z, y, x = shape
        return StackLayout(4, True, True, t, z, y, x)
    raise ValueError(f"Expected 2–4 dimensions, got {shape}")


def normalize_to_4d(data: np.ndarray, layout: StackLayout) -> np.ndarray:
    """Return array shaped (T, Z, Y, X)."""
    arr = np.asarray(data)
    if layout.ndim == 2:
        return arr.reshape(1, 1, layout.size_y, layout.size_x)
    if layout.ndim == 3:
        if layout.has_z:
            return arr.reshape(1, layout.size_z, layout.size_y, layout.size_x)
        return arr.reshape(layout.size_t, 1, layout.size_y, layout.size_x)
    return arr


def extract_slice(volume: np.ndarray, layout: StackLayout, t: int, z: int) -> np.ndarray:
    """Return a 2D (Y, X) slice from 2D–4D data."""
    vol4 = normalize_to_4d(volume, layout)
    t = max(0, min(t, vol4.shape[0] - 1))
    z = max(0, min(z, vol4.shape[1] - 1))
    return vol4[t, z]


def write_slice(
    volume: np.ndarray,
    layout: StackLayout,
    t: int,
    z: int,
    slice_2d: np.ndarray,
) -> np.ndarray:
    """Write a 2D slice back into a copy of ``volume``."""
    out = np.array(volume, copy=True)
    vol4 = normalize_to_4d(out, layout)
    t = max(0, min(t, vol4.shape[0] - 1))
    z = max(0, min(z, vol4.shape[1] - 1))
    vol4[t, z] = slice_2d
    if layout.ndim == 2:
        return vol4[0, 0]
    if layout.ndim == 3:
        if layout.has_z:
            return vol4[0]
        return vol4[:, 0]
    return vol4


def apply_brush(
    mask_slice: np.ndarray,
    y: int,
    x: int,
    radius: int,
    label: int,
    *,
    erase: bool = False,
) -> None:
    """Paint or erase a circular region in-place on a 2D mask slice."""
    h, w = mask_slice.shape
    r = max(1, int(radius))
    y0, y1 = max(0, y - r), min(h, y + r + 1)
    x0, x1 = max(0, x - r), min(w, x + r + 1)
    yy, xx = np.ogrid[y0:y1, x0:x1]
    dist2 = (yy - y) ** 2 + (xx - x) ** 2
    circle = dist2 <= r * r
    if erase:
        mask_slice[y0:y1, x0:x1][circle] = 0
    else:
        mask_slice[y0:y1, x0:x1][circle] = np.uint32(label)


def labels_to_rgba(mask_slice: np.ndarray, alpha: float = 0.45) -> np.ndarray:
    """Map label IDs to RGBA overlay (background transparent)."""
    h, w = mask_slice.shape
    rgba = np.zeros((h, w, 4), dtype=np.float32)
    labels = np.unique(mask_slice)
    labels = labels[labels > 0]
    if labels.size == 0:
        return rgba
    for label in labels:
        sel = mask_slice == label
        hue = (int(label) * 47) % 360
        # HSV to RGB simplified
        c = 0.85
        hp = hue / 60.0
        x = c * (1 - abs(hp % 2 - 1))
        if hp < 1:
            rgb = (c, x, 0)
        elif hp < 2:
            rgb = (x, c, 0)
        elif hp < 3:
            rgb = (0, c, x)
        elif hp < 4:
            rgb = (0, x, c)
        elif hp < 5:
            rgb = (x, 0, c)
        else:
            rgb = (c, 0, x)
        rgba[sel, 0] = rgb[0]
        rgba[sel, 1] = rgb[1]
        rgba[sel, 2] = rgb[2]
        rgba[sel, 3] = alpha
    return rgba
