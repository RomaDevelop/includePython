from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QBrush
from PySide6.QtWidgets import QTextEdit

class MyQTextEdit:
    @staticmethod
    def colorize_last_row(text_edit: QTextEdit, brush: QBrush):
        char_format = QTextCharFormat()
        char_format.setForeground(brush)

        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.setCharFormat(char_format)
        text_edit.repaint()

    @staticmethod
    def colorize_last_count(text_edit: QTextEdit, brush: QBrush, count):
        char_format = QTextCharFormat()
        char_format.setForeground(brush)

        cursor = text_edit.textCursor()
        cursor.setPosition(text_edit.document().characterCount() - 1 - count, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(char_format)
        text_edit.repaint()