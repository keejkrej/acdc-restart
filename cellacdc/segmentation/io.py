"""Load and save images and segmentation masks (Cell-ACDC compatible)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import tifffile

SEGM_SUFFIX = "segm.npz"
SEGM_KEY = "arr_0"


def segm_path_for_image(image_path: Path) -> Path:
    """Return default mask path: ``{stem}segm.npz`` next to the image."""
    return image_path.with_name(f"{image_path.stem}{SEGM_SUFFIX}")


def load_image(path: Path) -> np.ndarray:
    """Load a 2D–4D grayscale array from TIFF, NPY, or NPZ."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".tif", ".tiff"}:
        data = tifffile.imread(path)
    elif suffix == ".npy":
        data = np.load(path)
    elif suffix == ".npz":
        archive = np.load(path)
        key = SEGM_KEY if SEGM_KEY in archive else archive.files[0]
        data = archive[key]
    else:
        raise ValueError(f"Unsupported image format: {path.suffix}")

    data = np.asarray(data)
    if data.ndim < 2:
        raise ValueError(f"Image must be at least 2D, got shape {data.shape}")
    if data.ndim > 4:
        raise ValueError(f"Image must be at most 4D (T,Z,Y,X), got shape {data.shape}")
    return data


def load_mask(path: Path) -> np.ndarray:
    """Load a uint32 label mask from NPZ or NPY."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".npz":
        archive = np.load(path)
        if SEGM_KEY in archive:
            mask = archive[SEGM_KEY]
        else:
            mask = archive[archive.files[0]]
    elif suffix == ".npy":
        mask = np.load(path)
    else:
        raise ValueError(f"Unsupported mask format: {path.suffix}")
    return np.asarray(mask, dtype=np.uint32)


def save_mask(path: Path, mask: np.ndarray) -> None:
    """Save mask as compressed NPZ with key ``arr_0`` (Cell-ACDC convention)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **{SEGM_KEY: np.asarray(mask, dtype=np.uint32)})


def empty_mask_like(image: np.ndarray) -> np.ndarray:
    """Create a zero mask with the same dimensionality as ``image``."""
    return np.zeros(image.shape, dtype=np.uint32)
