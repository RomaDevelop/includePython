from PySide6.QtWidgets import QMessageBox

def qmb_error(text):
    QMessageBox.critical(None, "Error", text)