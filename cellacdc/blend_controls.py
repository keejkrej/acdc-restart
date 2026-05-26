"""Shared BF/fluor and image/segmentation crossfade sliders."""

from __future__ import annotations

from qtpy.QtCore import Qt, Signal
from qtpy.QtWidgets import QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget


class BlendControlBar(QWidget):
    """Bottom-bar crossfade controls used by 2D and 3D viewers."""

    bf_fluor_changed = Signal(int)
    image_seg_changed = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        self._image_seg_row = QWidget()
        image_seg_layout = QHBoxLayout(self._image_seg_row)
        image_seg_layout.setContentsMargins(0, 0, 0, 0)
        image_seg_layout.addWidget(QLabel("(BF/Fluor) ↔ Segmentation:"))
        self._image_seg_slider = QSlider(Qt.Horizontal)
        self._image_seg_slider.setRange(0, 100)
        self._image_seg_slider.setValue(50)
        self._image_seg_slider.valueChanged.connect(self.image_seg_changed.emit)
        image_seg_layout.addWidget(self._image_seg_slider, stretch=1)
        self._image_seg_label = QLabel("50%")
        self._image_seg_label.setMinimumWidth(48)
        image_seg_layout.addWidget(self._image_seg_label)
        self._image_seg_slider.valueChanged.connect(self._update_image_seg_label)
        layout.addWidget(self._image_seg_row)

        self._bf_fluor_row = QWidget()
        bf_fluor_layout = QHBoxLayout(self._bf_fluor_row)
        bf_fluor_layout.setContentsMargins(0, 0, 0, 0)
        self._bf_fluor_title = QLabel("BF ↔ Fluorescence:")
        bf_fluor_layout.addWidget(self._bf_fluor_title)
        self._bf_fluor_slider = QSlider(Qt.Horizontal)
        self._bf_fluor_slider.setRange(0, 100)
        self._bf_fluor_slider.setValue(50)
        self._bf_fluor_slider.valueChanged.connect(self.bf_fluor_changed.emit)
        bf_fluor_layout.addWidget(self._bf_fluor_slider, stretch=1)
        self._bf_fluor_label = QLabel("50%")
        self._bf_fluor_label.setMinimumWidth(48)
        bf_fluor_layout.addWidget(self._bf_fluor_label)
        self._bf_fluor_slider.valueChanged.connect(self._update_bf_fluor_label)
        layout.addWidget(self._bf_fluor_row)
        self._bf_fluor_row.setVisible(False)

    def _update_image_seg_label(self, value: int) -> None:
        self._image_seg_label.setText(f"{value}%")

    def _update_bf_fluor_label(self, value: int) -> None:
        self._bf_fluor_label.setText(f"{value}%")

    def set_values(
        self,
        *,
        bf_fluor: int,
        image_seg: int,
        show_bf_fluor: bool,
        channel_name: str = "",
    ) -> None:
        self._bf_fluor_row.setVisible(show_bf_fluor)
        if show_bf_fluor:
            title = (
                f"BF ↔ Fluorescence ({channel_name}):"
                if channel_name
                else "BF ↔ Fluorescence:"
            )
            self._bf_fluor_title.setText(title)
            self._bf_fluor_slider.blockSignals(True)
            self._bf_fluor_slider.setValue(bf_fluor)
            self._bf_fluor_slider.blockSignals(False)
            self._update_bf_fluor_label(bf_fluor)
        self._image_seg_slider.blockSignals(True)
        self._image_seg_slider.setValue(image_seg)
        self._image_seg_slider.blockSignals(False)
        self._update_image_seg_label(image_seg)
