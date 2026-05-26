"""Programmatic GUI session: ``imshow`` + ``run`` without mandatory filesystem I/O."""

from __future__ import annotations

import os
from dataclasses import dataclass

from cellacdc.data import Experiment, SegmentationResult, default_segmentation


@dataclass
class _Session:
    app: object
    presenter: object


_session: _Session | None = None


def _ensure_session() -> _Session:
    global _session
    if _session is not None:
        return _session

    os.environ.setdefault("QT_API", "pyside6")
    import pyqtgraph as pg
    from qtpy.QtWidgets import QApplication

    from cellacdc.segmentation.model import SegmentationModel
    from cellacdc.segmentation.presenter import SegmentationPresenter
    from cellacdc.segmentation.view import SegmentationView

    pg.setConfigOptions(imageAxisOrder="row-major")
    app = QApplication.instance() or QApplication([])
    model = SegmentationModel()
    view = SegmentationView()
    presenter = SegmentationPresenter(model, view)
    _session = _Session(app=app, presenter=presenter)
    return _session


def imshow(
    data: Experiment,
    *,
    result: SegmentationResult | None = None,
) -> None:
    """Open the segmentation viewer on ``data``, editing ``result`` in memory."""
    session = _ensure_session()
    mask_result = result if result is not None else default_segmentation(data)
    session.presenter.open(data, mask_result)
    session.presenter.run()


def run() -> int:
    """Start (or continue) the Qt event loop."""
    session = _ensure_session()
    return session.app.exec()
