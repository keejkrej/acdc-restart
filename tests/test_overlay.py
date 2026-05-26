"""Tests for multi-channel image loading."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from acdc.data import ImageData, coalesce_images
from acdc.segment.model import SegmentationModel
from acdc.volume.model import VolumeModel
from tests.test_experiment_io import _make_position


def test_from_path_channels_loads_each_channel(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    loaded = ImageData.from_path_channels(images, ["phase", "gfp"])
    assert len(loaded) == 2
    assert loaded[0].channel_name == "phase"
    assert loaded[1].channel_name == "gfp"
    assert loaded[0].image.shape == loaded[1].image.shape


def test_segmentation_model_multi_channel_open(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    channel_images = ImageData.from_path_channels(images, ["phase", "gfp"])
    from acdc.data import SegmentationResult

    result = SegmentationResult.empty_like(channel_images[0])
    model = SegmentationModel()
    model.open(channel_images, result)
    assert model.channels == channel_images
    assert len(model.current_channel_slices()) == 2
    assert model.current_channel_slices()[0].shape == (16, 16)
    model.set_channel_weights([0.25, 0.75])
    assert model.channel_weights == [0.25, 0.75]


def test_volume_model_stores_all_channels_on_bind(tmp_path: Path) -> None:
    images = _make_position(tmp_path, "Position_1")
    loaded = ImageData.from_path_channels(images, ["phase", "gfp"])
    model = VolumeModel()
    model.bind(loaded)
    assert model.channels == loaded
    model.bind(loaded[:1])
    assert model.channels == loaded[:1]


def test_coalesce_images_rejects_mismatched_shapes() -> None:
    a = ImageData.from_arrays(np.zeros((8, 8), dtype=np.uint8))
    b = ImageData.from_arrays(np.zeros((4, 4), dtype=np.uint8))
    with pytest.raises(ValueError, match="does not match"):
        coalesce_images([a, b])
