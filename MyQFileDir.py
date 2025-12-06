import os
import shutil
from functools import cmp_to_key

from PySide6.QtCore import qCritical, QDir, QFileInfo, QFile, QDateTime

class MyQFileDir:

    class ReadResult:
        def __init__(self, success: bool, content: str):
            self.success = success
            self.content = content

    @staticmethod
    def write_file(file_name, content, encoding="utf-8"):
        try:
            with open(file_name, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except LookupError:
            qCritical(f"MyQFileDir::WriteFile unknown codec [{encoding}]")
            return False
        except Exception as e:
            qCritical(f"MyQFileDir::WriteFile can't open file [{file_name}]: {e}")
            return False

    @staticmethod
    def read_file(file_name: str, encoding: str = None) -> ReadResult:
        # noinspection PyBroadException
        try:
            enc = encoding if encoding and encoding != "" else "utf-8"
            with open(file_name, "r", encoding=enc) as f:
                content = f.read()
            return MyQFileDir.ReadResult(True, content)
        except LookupError:
            qCritical(f"MyQFileDir::WriteFile unknown codec [{encoding}]")
            return MyQFileDir.ReadResult(False, "")
        except FileNotFoundError:
            qCritical(f"MyQFileDir::ReadFile2 can't open file [{file_name}]")
            return MyQFileDir.ReadResult(False, "")
        except OSError:
            qCritical(f"MyQFileDir::ReadFile2 can't read file [{file_name}]")
            return MyQFileDir.ReadResult(False, "")
        except Exception:
            qCritical(f"MyQFileDir::Exception [{file_name}]")
            return MyQFileDir.ReadResult(False, "")

    @staticmethod
    # return empty string if ok or error text
    # remove_old_remain_count -1 to disable remove
    def backup_file(file_name: str, backup_dir: str, prefix: str, remove_old_remain_count: int) -> str:
        ret_str = ""
        if not QFileInfo(backup_dir).isDir():
            if not QDir().mkpath(backup_dir):
                return "can't create dir " + backup_dir
        if remove_old_remain_count != -1:
            res_remove_old = MyQFileDir.remove_old_files(backup_dir, remove_old_remain_count)
            if res_remove_old: ret_str += f"warning: error removing old files: {res_remove_old}\n"
        backupFile = backup_dir + "/" + QDateTime.currentDateTime().toString("yyyy.MM.dd hh-mm-ss-zzz") + " "
        backupFile += prefix + " "
        backupFile += QFileInfo(file_name).fileName()
        if not QFile.copy(file_name, backupFile): ret_str += f"Can't copy base to {backup_dir}"
        return ret_str

    @staticmethod
    def get_dir_size(start_path: str):
        total_size = 0
        for dir_path, dir_names, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dir_path, f)
                # Пропускаем символические ссылки, чтобы избежать двойного счета или зацикливания
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    @staticmethod
    def remove_dir_with_content(directory: str) -> bool:
        try:
            shutil.rmtree(directory)
            return True
        except Exception as e:
            return False

    @staticmethod
    def RemoveFile(fileName: str) -> str:
        try:
            os.remove(fileName)
        except FileNotFoundError:
            return f"Ошибка: Файл {fileName} не найден."
        except PermissionError:
            return f"Ошибка: Недостаточно прав для удаления файла {fileName}."
        except Exception as e:
            return f"Произошла непредвиденная ошибка: {e} при удалении файла {fileName}."
        return ''

    class SortFlags:
        name = "name"
        modified = "modified"
        read = "read"
        no_sort = "noSort"

    @staticmethod
    def remove_old_files(directory_str: str, remain_count, sortFlag: SortFlags = SortFlags.modified):
        ret = ""
        directory = QDir(directory_str)
        if not directory.exists():
            ret += f"directory [{directory_str}] not exists"

        content = directory.entryInfoList(QDir.Filter.Files)
        i = len(content) - 1
        while i >= 0:
            if not content[i].isFile():
                content.pop(i)
            i -= 1

        def cmpName(a, b):
            return -1 if a.fileName() < b.fileName() else (1 if a.fileName() > b.fileName() else 0)

        def cmpModified(a, b):
            if a.lastModified() != b.lastModified():
                return -1 if a.lastModified() < b.lastModified() else 1
            return -1 if a.fileName() < b.fileName() else (1 if a.fileName() > b.fileName() else 0)

        def cmpRead(a, b):
            if a.lastRead() != b.lastRead():
                return -1 if a.lastRead() < b.lastRead() else 1
            return -1 if a.fileName() < b.fileName() else (1 if a.fileName() > b.fileName() else 0)

        if sortFlag == MyQFileDir.SortFlags.name:
            content = sorted(content, key=cmp_to_key(cmpName))
        elif sortFlag == MyQFileDir.SortFlags.modified:
            content = sorted(content, key=cmp_to_key(cmpModified))
        elif sortFlag == MyQFileDir.SortFlags.read:
            content = sorted(content, key=cmp_to_key(cmpRead))
        elif sortFlag == MyQFileDir.SortFlags.no_sort:
            pass
        else:
            ret += f"unreleased sort flag ({sortFlag})\n"

        while len(content) > remain_count:
            if not QFile(content[0].filePath()).remove():
                ret += f"can't remove file [{content[-1].filePath()}]\n"
            content.pop(0)

        return ret