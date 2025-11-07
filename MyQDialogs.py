from collections.abc import Sequence
from typing import List

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QWidget, QDialog, QMessageBox, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QListWidget

from my_shortings import qmb_error


class MyQDialogs:

    @staticmethod
    def show_text(captionDialog: str, text: str = '', w: int = 640, h: int = 480):
        dialog = QDialog()
        dialog.setWindowTitle(captionDialog)

        vloAll = QVBoxLayout(dialog)
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setTabStopDistance(40)
        textEdit.setText(text)
        vloAll.addWidget(textEdit)
        dialog.resize(w, h)
        dialog.exec()

    class InputTextRes:
        def __init__(self):
            self.accepted = False
            self.text = ""

    @staticmethod
    def input_text(caption_dialog: str, start_text: str = '', w: int = 640, h: int = 480) -> InputTextRes:
        dialog = QDialog()
        res = MyQDialogs.InputTextRes()
        dialog.setWindowTitle(caption_dialog)

        vlo_all = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setTabStopDistance(40)
        text_edit.setText(start_text)
        text_edit.setAcceptRichText(False)
        vlo_all.addWidget(text_edit)

        hlo_buttons = QHBoxLayout()
        vlo_all.addLayout(hlo_buttons)

        hlo_buttons.addStretch()
        accept_btn = QPushButton("Accept")
        hlo_buttons.addWidget(accept_btn)
        def _on_accept():
            res.accepted = True
            res.text = text_edit.toPlainText()
            dialog.close()
        accept_btn.clicked.connect(_on_accept)

        cancel_btn = QPushButton("Cancel")
        hlo_buttons.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.close)

        dialog.resize(w, h)
        dialog.exec()

        return res

    class ListDialogRes:
        def __init__(self):
            self.accepted = False
            self.chosenIndex = -1
            self.chosenText = ""

    @staticmethod
    def list_dialog(caption_dialog: str, values: Sequence[str], w: int = 640, h: int = 480) -> ListDialogRes:
        dialog = QDialog()
        res = MyQDialogs.ListDialogRes()
        dialog.setWindowTitle(caption_dialog)

        vlo_all = QVBoxLayout(dialog)
        list_widget = QListWidget()
        list_widget.addItems(values)
        vlo_all.addWidget(list_widget)

        hlo_buttons = QHBoxLayout()
        vlo_all.addLayout(hlo_buttons)

        hlo_buttons.addStretch()
        accept_btn = QPushButton("Accept")
        hlo_buttons.addWidget(accept_btn)
        def _on_accept():
            item = list_widget.currentItem()
            if not item:
                qmb_error("Choose value or press cansel or close")
                return
            res.accepted = True
            res.chosenText = item.text()
            res.chosenIndex = list_widget.currentRow()
            dialog.close()

        list_widget.itemDoubleClicked.connect(_on_accept)
        accept_btn.clicked.connect(_on_accept)

        cancel_btn = QPushButton("Cancel")
        hlo_buttons.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.close)

        dialog.resize(w, h)
        dialog.exec()

        return res

    class MenuItem:
        SEPARATOR = 'separator'

        def __init__(self, text, worker):
            self.text = text
            self.worker = worker

        @staticmethod
        def separator():
            return MyQDialogs.MenuItem(MyQDialogs.MenuItem.SEPARATOR, None)

    @staticmethod
    def menu_in_pos(pos: QPoint, items: list[MenuItem], parent: QWidget = None):
        menu = QMenu(parent)

        '''
        items = [
            MyQDialogs.MenuItem("Option 1", lambda: print("1")),
            MyQDialogs.MenuItem("Option 2", lambda: print("2")),
        ]
        MyQDialogs.menu_in_pos(pos, items, widget)
        MyQDialogs.menu_under_widget(row_in_table.btnOther, items)
        '''

        def trigger_action(menu_item: MyQDialogs.MenuItem):
            menu_item.worker()

        for item in items:
            if item.text == MyQDialogs.MenuItem.SEPARATOR: menu.addSeparator()
            else:
                if not item.worker:
                    qmb_error("nullptr worker in action " + item.text)
                    continue

                action = QAction(item.text, menu)
                menu.addAction(action)
                action.triggered.connect(lambda _, item_copy=item: trigger_action(item_copy))

        menu.exec(pos)

    @staticmethod
    def menu_under_widget(widget: QWidget, items: list[MenuItem]):
        menu = QMenu(widget)

        MyQDialogs.menu_in_pos(widget.mapToGlobal(QPoint(1, widget.height())), items, widget)

    @staticmethod
    def custom_dialog(caption: str, text: str, buttons: list[str]) -> str:
        messageBox = QMessageBox(QMessageBox.Icon.Question, caption, text)
        for btn in buttons:
            messageBox.addButton(" " + btn + " ", QMessageBox.ButtonRole.YesRole) # Role не имеет значения
            # добавлены пробелы потому что setContentsMargins для вн.виджетов, а не текста,
            # а setStyleSheet("padding: 6px;") имеет побочные эффекты

        messageBox.exec()
        retText: str
        if messageBox.clickedButton(): retText = messageBox.clickedButton().text()[1:-1] # [1:-1] удаление пробелов
        else: retText = ''
        return retText