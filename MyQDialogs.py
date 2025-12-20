from collections.abc import Sequence
from typing import List

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QWidget, QDialog, QMessageBox, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QListWidget, QCheckBox, QListWidgetItem

from my_shortings import qmb_error


class MyQDialogs:

    @staticmethod
    def show_text(captionDialog: str, text: str, w: int = 640, h: int = 480):
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

        def __init__(self, text, worker, childItems = None):
            self.text = text
            self.worker = worker
            self.childItems = childItems

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

        def add_items_in_menu(a_items, a_menu: QMenu):
            for item in a_items:
                if item.text == MyQDialogs.MenuItem.SEPARATOR:
                    a_menu.addSeparator()
                else:
                    if item.childItems:
                        submenu = QMenu(item.text, a_menu)
                        a_menu.addMenu(submenu)
                        add_items_in_menu(item.childItems, submenu)
                        if item.worker: qmb_error("worker on submenu, it can't be called")
                    else:
                        if not item.worker:
                            qmb_error("nullptr worker in action " + item.text)
                            continue

                        action = QAction(item.text, a_menu)
                        a_menu.addAction(action)
                        action.triggered.connect(lambda _, item_copy=item: trigger_action(item_copy))

        add_items_in_menu(items, menu)

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

    class CheckBoxDialogItem:
        def __init__(self, text="", checkState=False, enabled=True):
            self.text = text
            self.checkState = checkState
            self.enabled = enabled

    class CheckBoxDialogResult:
        def __init__(self):
            self.allItems = []  # list[CheckBoxDialogItem]
            self.checkedItems = []  # list[CheckBoxDialogItem]
            self.checkedIndexes = []  # list[int]
            self.checkedTexts = []  # list[str]
            self.accepted = False

    @staticmethod
    def check_box_dialog(caption, items_or_values, startChecked=None, enabled=None,
                         startAllChecked=False, w=640, h=480):

        # Перегрузка логики: если пришел список объектов CheckBoxDialogItem
        if isinstance(items_or_values, list) and len(items_or_values) > 0 \
                and isinstance(items_or_values[0], MyQDialogs.CheckBoxDialogItem):
            values = [item.text for item in items_or_values]
            startChecked = [item.checkState for item in items_or_values]
            enabled = [item.enabled for item in items_or_values]
            return MyQDialogs._CheckBoxDialog(caption, values, startChecked,
                                              enabled, False, w, h)

        # Обычный вызов со строками
        return MyQDialogs._CheckBoxDialog(caption, items_or_values, startChecked or [],
                                          enabled or [], startAllChecked, w, h)

    @staticmethod
    def _CheckBoxDialog(caption, values, startChecked, enabled, startAllChecked, w, h):
        result = MyQDialogs.CheckBoxDialogResult()

        dialog = QDialog()
        dialog.resize(w, h)
        dialog.setWindowTitle(caption)

        vloMain = QVBoxLayout(dialog)
        hloHeader = QHBoxLayout()
        listWidget = QListWidget()
        chBoxAllCheck = QCheckBox("Check All")  # В С++ тексты из функций Accept()/Cansel()
        chBoxAllUncheck = QCheckBox("Uncheck All")  # здесь для наглядности

        hloBottom = QHBoxLayout()
        btnOk = QPushButton("OK")
        btnCancel = QPushButton("Cancel")

        # Лямбды для кнопок
        btnOk.clicked.connect(lambda: (setattr(result, 'accepted', True), dialog.hide()))
        btnCancel.clicked.connect(lambda: (setattr(result, 'accepted', False), dialog.hide()))

        vloMain.addLayout(hloHeader)
        hloHeader.addWidget(chBoxAllCheck)
        hloHeader.addWidget(chBoxAllUncheck)
        hloHeader.addStretch()
        vloMain.addWidget(listWidget)
        vloMain.addLayout(hloBottom)
        hloBottom.addStretch()
        hloBottom.addWidget(btnOk)
        hloBottom.addWidget(btnCancel)

        # all check
        chBoxAllCheck.setChecked(True)

        def on_all_check():
            for i in range(listWidget.count()):
                item = listWidget.item(i)

                if item.flags() & Qt.ItemFlag.ItemIsEnabled:
                    item.setCheckState(Qt.CheckState.Checked)
            chBoxAllCheck.setChecked(True)

        chBoxAllCheck.clicked.connect(on_all_check)

        # all uncheck
        chBoxAllUncheck.setChecked(False)

        def on_all_uncheck():
            for i in range(listWidget.count()):
                item = listWidget.item(i)
                if item.flags() & Qt.ItemFlag.ItemIsEnabled:
                    item.setCheckState(Qt.CheckState.Unchecked)
            chBoxAllUncheck.setChecked(False)

        chBoxAllUncheck.clicked.connect(on_all_uncheck)

        # двойной клик
        def on_double_click(item):
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)
            else:
                item.setCheckState(Qt.CheckState.Checked)

        listWidget.itemDoubleClicked.connect(on_double_click)

        # добавление строк
        for i, str_val in enumerate(values):
            item = QListWidgetItem(str_val)
            item.setCheckState(Qt.CheckState.Unchecked)

            if startAllChecked:
                item.setCheckState(Qt.CheckState.Checked)

            if i < len(startChecked) and startChecked[i]:
                item.setCheckState(Qt.CheckState.Checked)

            if i < len(enabled) and not enabled[i]:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

            listWidget.addItem(item)

        # запуск
        dialog.exec()

        # подготовка результата
        if result.accepted:
            for i in range(listWidget.count()):
                widget_item = listWidget.item(i)
                is_checked = widget_item.checkState() == Qt.CheckState.Checked
                is_enabled = bool(widget_item.flags() & Qt.ItemFlag.ItemIsEnabled)

                res_item = MyQDialogs.CheckBoxDialogItem(widget_item.text(), is_checked, is_enabled)
                result.allItems.append(res_item)

                if is_checked:
                    result.checkedItems.append(res_item)
                    result.checkedIndexes.append(i)
                    result.checkedTexts.append(res_item.text)

        return result