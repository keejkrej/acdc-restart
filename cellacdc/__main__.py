"""Entry point for the manual segmentation GUI."""

from __future__ import annotations

import os
import sys


def main() -> None:
    os.environ.setdefault("QT_API", "pyside6")
    from cellacdc.segmentation.presenter import create_app

    app, presenter = create_app()
    presenter.run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
