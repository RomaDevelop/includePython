from PySide6.QtWidgets import QMessageBox

def qmb_error(text):
    QMessageBox.critical(None, "Error", text)           # type: ignore

def qmb_info(text):
    QMessageBox.information(None, "Error", text)        # type: ignore

DateTimeFormat = "yyyy.MM.dd hh:mm:ss"
DateTimeFormat_ms = "yyyy.MM.dd hh:mm:ss.zzz"
DateTimeFormatForFileName = "yyyy.MM.dd hh-mm-ss"
DateTimeFormatForFileName_ms = "yyyy.MM.dd hh-mm-ss-zzz"