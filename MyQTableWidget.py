from PySide6.QtWidgets import QTableWidget

class MyQTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disableKeyboardSearch = False

    def keyboardSearch(self, search: str):
        if self.disableKeyboardSearch:
            return
        super().keyboardSearch(search)
