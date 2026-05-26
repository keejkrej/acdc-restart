"""Cell-ACDC minimal manual segmentation GUI."""

from acdc.app import get_qapp, run
from acdc.data import ImageData, SegmentationResult, load
from acdc.segment.viewer import SegmentationViewer, current_viewer, segment
from acdc.volume.viewer import VolumeViewer, current_volume_viewer, volume

__all__ = [
    "ImageData",
    "SegmentationResult",
    "SegmentationViewer",
    "VolumeViewer",
    "current_viewer",
    "current_volume_viewer",
    "get_qapp",
    "load",
    "run",
    "segment",
    "volume",
    "__version__",
]

__version__ = "0.1.0"
