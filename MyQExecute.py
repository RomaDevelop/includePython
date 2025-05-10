from PySide6.QtCore import QFileInfo, QDir, QUrl, QProcess
from PySide6.QtGui import QDesktopServices

class MyQExecute:
    @staticmethod
    def show_in_explorer(file_or_dir: str) -> bool:
        file_info = QFileInfo(file_or_dir)
        if not file_info.isSymLink() and (file_info.isFile() or file_info.isDir()):
            args = ["/select,", QDir.toNativeSeparators(file_or_dir)]
            return QProcess.startDetached("explorer", args)[0]
        else:
            print(f"my_execute::show_in_explorer: объект {file_or_dir} не обнаружен")
            return False

    @staticmethod
    def execute(file, args=None):
        ERROR_PREFIX = "MyQExecute::Execute: объект " + file
        do_open_url = False

        file_info = QFileInfo(file)

        if not file_info.exists():
            print(ERROR_PREFIX + " не существует")
            return False

        if file_info.isSymLink():
            do_open_url = True  # если ярлык - запустим через QDesktopServices
        elif file_info.isFile():
            if file_info.isExecutable():  # Если файл исполняемый
                start_res = QProcess.startDetached(file, args if args is not None else [])  # запускем через QProcess
                if not start_res:
                    print(ERROR_PREFIX + ": QProcess::startDetached returned false")
                return start_res
            else:
                do_open_url = True  # если нет - запустим через QDesktopServices

        if do_open_url:
            if args:
                print(ERROR_PREFIX + " не является исполняемым, аргументы игнорируются")
            open_res = QDesktopServices.openUrl(QUrl.fromLocalFile(file))
            if not open_res:
                print(ERROR_PREFIX + ": QDesktopServices::openUrl returned false")
            return open_res

        print(ERROR_PREFIX + " не был запущен, не известный формат")
        return False

    @staticmethod
    def open_dir(directory):
        file_info = QFileInfo(directory)

        if not file_info.isSymLink() and file_info.isDir():
            args = [QDir.toNativeSeparators(directory)]
            return QProcess.startDetached("explorer", args)

        print("MyQExecute::Execute: директория " + directory + " не обнаружена")
        return False