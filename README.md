# acdc-restart

Minimal **manual segmentation** GUI for microscopy, rewritten from [Cell_ACDC](https://github.com/keejkrej/Cell_ACDC) segmentation mode using **Model–View–Presenter**. No model inference, no custom Qt styling.

## Features

- Open Cell-ACDC experiment folders (`Position_n/Images/`) or individual image files
- Position and channel pickers for multi-position experiments; multi-select channel picker at load
- Brush and eraser with configurable label ID and brush size
- Frame and Z-slice navigation for stacks
- Mask overlay toggle
- Undo / redo
- Save masks as `{basename}segm.npz` with key `arr_0` (`uint32`), compatible with Cell-ACDC
- 3D volume viewer (`acdc-3d`) with vispy overlay, segmentation-style shell (hand tool, labels dock, frame transport)

## Opening data

Primary workflow: **File → Open folder** and select any of:

- Experiment root (contains `Position_1/`, `Position_2/`, …)
- A single `Position_n/` folder
- A `Position_n/Images/` folder directly

Channel files are resolved as `{basename}{channel}_aligned.npz` (preferred) or `{basename}{channel}.tif`. Masks load/save as `{basename}segm.npz` in the same `Images/` folder.

Use **File → Open image file** for loose TIFF/NPY/NPZ outside the Cell-ACDC layout.

## Requirements

- Python 3.12 (pinned via `uv`)
- qtpy + PySide6 + pyqtgraph + vispy

## Install and run

```bash
uv sync
uv run acdc-seg    # 2D manual segmentation
uv run acdc-3d     # 3D volume viewer
```

## Programmatic API

Load data, edit in the 2D viewer, optionally inspect in 3D, then continue your script:

```python
import acdc

images, segmentation = acdc.load("/path/to/experiment", channels=["phase", "gfp"])
images, segmentation = acdc.segment(images, segmentation)
images, segmentation = acdc.volume(images, segmentation)

segmentation.save()  # or downstream analysis on segmentation.mask
```

Build data yourself when you need full control:

```python
images = acdc.ImageData.from_path_channels("/path/to/experiment", ["phase", "gfp"])
segmentation = acdc.segmentResult.empty_like(images[0])
# or: segmentation = acdc.segmentResult.from_path("mask.npz", like=images[0])

images, segmentation = acdc.segment(images, segmentation)
```

- **`load(path, channel=..., channels=..., position=...)`** — returns `(images, segmentation)`; loads an existing mask from disk when present, otherwise a new empty mask
- **`ImageData`** — read-only image volume + layout metadata
- **`SegmentationResult`** — label mask (`uint32`); edited in 2D, overlaid in 3D
- **`segment(images, segmentation)`** — 2D manual segmentation; blocks until the window closes; returns `(images, segmentation)` (same objects, possibly mutated in place)
- **`volume(images, segmentation, t_index=0)`** — 3D read-only overlay; same blocking/return behavior
- **`run()`** — only needed for CLI-style apps that keep a window open without `segment` (`uv run acdc-seg` or `uv run acdc-3d`)

3D viewer: dual LUT bars (image grey, labels viridis) and an **Image ↔ Segmentation** blend slider; vispy default volume rendering only (no exposed render controls).

## Layout

```
acdc/
  __init__.py              # Public API
  app.py                   # get_qapp, run
  data.py                  # ImageData + SegmentationResult
  segment/
    __main__.py            # acdc-seg CLI
    viewer.py              # SegmentationViewer, segment
    model.py               # Editing state (binds to SegmentationResult)
    view.py                # Qt / pyqtgraph UI
    presenter.py           # MVP wiring
    experiment.py          # Cell-ACDC folder discovery
    io.py                  # Cell-ACDC mask format
    tools.py               # Brush math and stack helpers
  volume/
    viewer.py              # VolumeViewer, volume (vispy)
    __main__.py            # acdc-3d CLI
```

## License

BSD-3-Clause (see upstream Cell-ACDC).
