import os
import ctypes
from ctypes import wintypes

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
