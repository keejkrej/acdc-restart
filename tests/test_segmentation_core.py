"""Unit tests for manual segmentation core (no GUI)."""

from pathlib import Path

import numpy as np

from cellacdc.segmentation import io, tools
from cellacdc.segmentation.model import SegmentationModel


def test_apply_brush_and_save_roundtrip(tmp_path: Path) -> None:
    image = np.zeros((32, 48), dtype=np.uint16)
    image[10:20, 10:30] = 1000
    image_path = tmp_path / "cell.tif"
    import tifffile

    tifffile.imwrite(image_path, image)

    model = SegmentationModel()
    model.load_image(image_path)
    sl = model.current_mask_slice()
    tools.apply_brush(sl, 15, 15, radius=3, label=2)
    model.set_mask_slice(sl)

    out = tmp_path / "cellsegm.npz"
    model.save_mask(out)
    loaded = io.load_mask(out)
    assert loaded.dtype == np.uint32
    assert loaded.shape == image.shape
    assert loaded[15, 15] == 2


def test_infer_layout_3d_z() -> None:
    layout = tools.infer_layout((8, 64, 64))
    assert layout.has_z and not layout.has_time
    assert layout.size_z == 8


def test_undo(tmp_path: Path) -> None:
    image = np.ones((16, 16), dtype=np.uint8)
    image_path = tmp_path / "a.npy"
    np.save(image_path, image)
    model = SegmentationModel()
    model.load_image(image_path)
    model.begin_stroke()
    model.paint(5, 5)
    model.end_stroke()
    assert model.current_mask_slice()[5, 5] != 0
    assert model.undo()
    assert model.current_mask_slice()[5, 5] == 0
