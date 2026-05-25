"""Manual segmentation mode (MVP architecture)."""

__all__ = [
    "SegmentationModel",
    "SegmentationPresenter",
    "SegmentationView",
]


def __getattr__(name: str):
    if name == "SegmentationModel":
        from .model import SegmentationModel

        return SegmentationModel
    if name == "SegmentationPresenter":
        from .presenter import SegmentationPresenter

        return SegmentationPresenter
    if name == "SegmentationView":
        from .view import SegmentationView

        return SegmentationView
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
