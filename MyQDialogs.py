from typing import List

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu,QWidget, QDialog, QMessageBox, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

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
    def input_text(captionDialog: str, startText: str = '', w: int = 640, h: int = 480) -> InputTextRes:
        dialog = QDialog()
        res = MyQDialogs.InputTextRes()
        dialog.setWindowTitle(captionDialog)

        vloAll = QVBoxLayout(dialog)
        textEdit = QTextEdit()
        textEdit.setTabStopDistance(40)
        textEdit.setText(startText)
        textEdit.setAcceptRichText(False)
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

    class MenuItem:
        SEPARATOR = 'separator'

        def __init__(self, text, worker):
            self.text = text
            self.worker = worker

        @staticmethod
        def separator():
            return MyQDialogs.MenuItem(MyQDialogs.MenuItem.SEPARATOR, None)

    @staticmethod
    def menu_under_widget(widget: QWidget, items: list[MenuItem]):
        menu = QMenu(widget)

        # обработка действия
        def trigger_action(menu_item: MyQDialogs.MenuItem):
            menu_item.worker()

        # сохранение замыкания
        for item in items:
            if item.text == MyQDialogs.MenuItem.SEPARATOR: menu.addSeparator()
            else:
                if not item.worker:
                    qmb_error("nullptr worker in action " + item.text)
                    continue

                action = QAction(item.text, menu)
                menu.addAction(action)
                action.triggered.connect(lambda _, item_copy=item: trigger_action(item_copy))

        menu.exec(widget.mapToGlobal(QPoint(1, widget.height())))

        '''
        items = [
            MyQDialogs.MenuItem("Option 1", lambda: print("1")),
            MyQDialogs.MenuItem("Option 2", lambda: print("2")),
        ]
        MyQDialogs.menu_under_widget(row_in_table.btnOther, items)
        '''

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