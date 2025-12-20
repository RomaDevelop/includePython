from PySide6.QtWidgets import QTableWidget

class MyQTableWidget(QTableWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disableKeyboardSearch = False

    def keyboardSearch(self, search: str):
        if self.disableKeyboardSearch:
            return
        super().keyboardSearch(search)

    def save_cols_visibility(self) -> str:
        columns_visible = ''
        for col in range(self.columnCount()): columns_visible += '0,' if self.isColumnHidden(col) else '1,'
        columns_visible = columns_visible[:-1]
        return columns_visible

    def load_cols_visibility(self, saved_value: str):
        columns_visible_vals = saved_value.split(',')
        col = 0
        for val in columns_visible_vals:
            if self.columnCount() <= col:
                print(f'load_cols_visibility: bad column index {col}')
            self.setColumnHidden(col, val == '0')
            col += 1
