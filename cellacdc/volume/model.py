"""Read-only state for the 3D volume viewer."""

from __future__ import annotations

import numpy as np

from cellacdc.data import ImagedData, SegmentationResult, default_segmentation
from cellacdc.overlay import FluorescenceOverlay


class VolumeModel:
    """Holds loaded image/mask volumes for 3D display."""

    def __init__(self) -> None:
        self.imaged: ImagedData | None = None
        self.result: SegmentationResult | None = None
        self.t_index = 0
        self.label_id = 1
        self.fluorescence: FluorescenceOverlay | None = None
        self.bf_fluor_blend = 50.0
        self.image_seg_blend = 50.0

    @property
    def has_data(self) -> bool:
        return self.imaged is not None and self.result is not None

    def bind(self, imaged: ImagedData, result: SegmentationResult | None = None) -> SegmentationResult:
        mask = result if result is not None else default_segmentation(imaged)
        self.imaged = imaged
        self.result = mask
        self.t_index = 0
        self.fluorescence = None
        return mask

    def fluorescence_sibling_channels(self) -> list[str]:
        if self.imaged is None or self.imaged.images_path is None:
            return []
        from cellacdc.overlay import list_sibling_channels

        return list_sibling_channels(
            self.imaged.images_path,
            exclude=self.imaged.channel_name,
        )

    def load_fluorescence_channel(self, channel_name: str) -> None:
        if self.imaged is None or self.imaged.images_path is None:
            raise ValueError("Fluorescence overlay requires a Cell-ACDC Images folder")
        from cellacdc.overlay import load_channel_image

        image = load_channel_image(
            self.imaged.images_path,
            channel_name,
            layout=self.imaged.layout,
        )
        self.fluorescence = FluorescenceOverlay(channel_name, image)

    def clear_fluorescence(self) -> None:
        self.fluorescence = None

    def set_bf_fluor_blend(self, value_0_to_100: float) -> None:
        self.bf_fluor_blend = max(0.0, min(100.0, float(value_0_to_100)))

    def set_image_seg_blend(self, value_0_to_100: float) -> None:
        self.image_seg_blend = max(0.0, min(100.0, float(value_0_to_100)))

    def all_label_ids(self) -> list[int]:
        if not self.has_data or self.result is None:
            return []
        ids = np.unique(self.result.mask)
        return sorted(int(label) for label in ids if label > 0)

    def status_label(self) -> str:
        if self.imaged is not None and self.imaged.title:
            return self.imaged.title
        if self.imaged is not None and self.imaged.image_path is not None:
            return self.imaged.image_path.name
        return ""
