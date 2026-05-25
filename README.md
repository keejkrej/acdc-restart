# acdc-restart

Minimal **manual segmentation** GUI for microscopy, rewritten from [Cell_ACDC](https://github.com/keejkrej/Cell_ACDC) segmentation mode using **Model–View–Presenter**. No model inference, no custom Qt styling.

## Features

- Open 2D–4D images (TIFF, NPY, NPZ)
- Brush and eraser with configurable label ID and brush size
- Frame and Z-slice navigation for stacks
- Mask overlay toggle
- Undo / redo
- Save masks as `{image_stem}segm.npz` with key `arr_0` (`uint32`), compatible with Cell-ACDC

## Requirements

- Python 3.12 (pinned via `uv`)
- qtpy + PySide6 + pyqtgraph

## Install and run

```bash
uv sync
uv run acdc-seg
```

## Layout

```
src/cellacdc/
  __main__.py              # CLI entry
  segmentation/
    model.py               # State and I/O orchestration
    view.py                # Qt / pyqtgraph UI
    presenter.py           # MVP wiring
    io.py                  # Cell-ACDC mask format
    tools.py               # Brush math and stack helpers
```

## License

BSD-3-Clause (see upstream Cell-ACDC).
