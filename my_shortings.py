from PySide6.QtWidgets import QMessageBox

def qmb_error(text):
    QMessageBox.critical(None, "Error", text)           # type: ignore

def qmb_info(text):
    QMessageBox.information(None, "Error", text)        # type: ignore