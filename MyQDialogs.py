from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

class MyQDialogs:

    class InputTextRes:
        def __init__(self):
            self.accepted = False
            self.text = ""

    @staticmethod
    def InputText(captionDialog: str, startText: str = '', w: int = 640, h: int = 480) -> InputTextRes:
        dialog = QDialog()
        res = MyQDialogs.InputTextRes()
        dialog.setWindowTitle(captionDialog)

        vloAll = QVBoxLayout(dialog)
        textEdit = QTextEdit()
        textEdit.setTabStopDistance(40)
        textEdit.setText(startText)
        vloAll.addWidget(textEdit)

        hloButtons = QHBoxLayout()
        vloAll.addLayout(hloButtons)

        hloButtons.addStretch()
        acceptBtn = QPushButton("Accept")
        hloButtons.addWidget(acceptBtn)
        def _on_accept():
            res.accepted = True
            res.text = textEdit.toPlainText()
            dialog.close()
        acceptBtn.clicked.connect(_on_accept)

        cancelBtn = QPushButton("Cancel")
        hloButtons.addWidget(cancelBtn)
        cancelBtn.clicked.connect(dialog.close)

        dialog.resize(w, h)
        dialog.exec()

        return res