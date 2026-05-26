"""Shared Qt dialogs."""

from __future__ import annotations

from qtpy.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QWidget,
)


def pick_from_list(parent: QWidget, title: str, names: list[str]) -> str | None:
    """Show a list picker dialog and return the selected name."""
    if not names:
        return None
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel(f"{title}:"))
    list_widget = QListWidget()
    list_widget.addItems(names)
    list_widget.setCurrentRow(0)
    list_widget.itemDoubleClicked.connect(dialog.accept)
    layout.addWidget(list_widget)
    buttons = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
        parent=dialog,
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    if dialog.exec() != QDialog.Accepted:
        return None
    selected = list_widget.currentItem()
    return selected.text() if selected is not None else None
