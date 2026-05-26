"""Tests for optional fluorescence overlay channel loading."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import tifffile

from cellacdc.overlay import list_sibling_channels, load_channel_image
from cellacdc.segmentation import io, tools
from cellacdc.segmentation.model import SegmentationModel
from cellacdc.volume.model import VolumeModel
from tests.test_experiment_io import _make_position, _write_metadata


def test_list_sibling_channels_excludes_primary(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    channels = list_sibling_channels(images)
    assert sorted(channels) == ["gfp", "phase"]
    assert list_sibling_channels(images, exclude="phase") == ["gfp"]


def test_load_channel_image_validates_shape(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    layout = tools.layout_from_metadata((16, 16), size_t=1, size_z=1)
    phase = load_channel_image(images, "phase", layout=layout)
    assert phase.shape == (16, 16)

    bad = np.zeros((8, 8), dtype=np.uint16)
    tifffile.imwrite(images / "test_s01_mCherry.tif", bad)
    _write_metadata(
        images,
        "test_s01_",
        channels=("phase", "gfp", "mCherry"),
    )
    with pytest.raises(ValueError, match="does not match"):
        load_channel_image(images, "mCherry", layout=layout)


def test_segmentation_model_fluorescence_overlay(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    model = SegmentationModel()
    spec = __import__("cellacdc.segmentation.experiment", fromlist=["build_load_spec"]).build_load_spec(
        images, "phase"
    )
    model.load_position(spec)
    assert model.fluorescence_sibling_channels() == ["gfp"]
    model.load_fluorescence_channel("gfp")
    assert model.fluorescence is not None
    assert model.fluorescence.channel_name == "gfp"
    slice_ = model.current_fluorescence_slice()
    assert slice_ is not None and slice_.shape == (16, 16)
    model.set_bf_fluor_blend(25)
    assert model.bf_fluor_blend == 25
    model.set_image_seg_blend(75)
    assert model.image_seg_blend == 75
    model.clear_fluorescence()
    assert model.fluorescence is None


def test_volume_model_clears_fluorescence_on_bind(tmp_path: Path) -> None:
    from cellacdc.data import ImagedData

    images = _make_position(tmp_path, "Position_1")
    imaged = ImagedData.from_path(images, channel="phase")
    model = VolumeModel()
    model.bind(imaged)
    model.load_fluorescence_channel("gfp")
    assert model.fluorescence is not None
    model.bind(imaged)
    assert model.fluorescence is None
