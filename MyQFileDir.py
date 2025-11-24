import os
import shutil

from PySide6.QtCore import qCritical

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
