import os
import ctypes
from ctypes import wintypes

import win32gui
import win32con

from PySide6.QtCore import QTimer

class PlatformDependent:
    @staticmethod
    def open_file_properties(filepath: str) -> bool:
        if not os.path.exists(filepath):
            return False

        SEE_MASK_INVOKEIDLIST = 0x0000000C

        class SHELLEXECUTEINFO(ctypes.Structure):
            _fields_ = [
                ('cbSize',          wintypes.DWORD),
                ('fMask',           wintypes.ULONG),
                ('hwnd',            wintypes.HWND),
                ('lpVerb',          wintypes.LPCWSTR),
                ('lpFile',          wintypes.LPCWSTR),
                ('lpParameters',    wintypes.LPCWSTR),
                ('lpDirectory',     wintypes.LPCWSTR),
                ('nShow',           ctypes.c_int),
                ('hInstApp',        wintypes.HINSTANCE),
                ('lpIDList',        ctypes.c_void_p),
                ('lpClass',         wintypes.LPCWSTR),
                ('hkeyClass',       wintypes.HKEY),
                ('dwHotKey',        wintypes.DWORD),
                ('hIcon',           wintypes.HANDLE),
                ('hProcess',        wintypes.HANDLE),
            ]

        ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(sei)
        sei.fMask = SEE_MASK_INVOKEIDLIST
        sei.hwnd = None
        sei.lpVerb = "properties"
        sei.lpFile = filepath
        sei.lpParameters = None
        sei.lpDirectory = None
        sei.nShow = 1
        sei.hInstApp = None

        ShellExecuteEx(ctypes.byref(sei))
        return True

    @staticmethod
    def set_foreground(window):
        """ Работает только для поднятия на верхний уровень, например при нажатии иконки в трее,
                но если set_foreground вызвано внутренним событием приложения -
                не срабатывает, вероятно из-за защиты Windows """
        hwnd = int(window.winId())
        win32gui.SetForegroundWindow(hwnd)

    @staticmethod
    def set_top_most(window, top_most: bool):
        hwnd = int(window.winId())
        z_order = win32con.HWND_TOPMOST if top_most else win32con.HWND_NOTOPMOST
        flags = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
        win32gui.SetWindowPos(hwnd, z_order, 0, 0, 0, 0, flags)

    @staticmethod
    def set_top_most_flash(window):
        PlatformDependent.set_top_most(window, True)
        #PlatformDependent.set_top_most(window, False)
        QTimer.singleShot(100, lambda : PlatformDependent.set_top_most(window, False))