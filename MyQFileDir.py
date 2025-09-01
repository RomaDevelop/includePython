from PySide6.QtCore import qCritical

class MyQFileDir:

    class ReadResult:
        def __init__(self, success: bool, content: str):
            self.success = success
            self.content = content

    @staticmethod
    def WriteFile(fileName, content, encoding="utf-8"):
        try:
            with open(fileName, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except LookupError:
            qCritical(f"MyQFileDir::WriteFile unknown codec [{encoding}]")
            return False
        except Exception as e:
            qCritical(f"MyQFileDir::WriteFile can't open file [{fileName}]: {e}")
            return False

    @staticmethod
    def ReadFile(fileName: str, encoding: str = None) -> ReadResult:
        # noinspection PyBroadException
        try:
            enc = encoding if encoding and encoding != "" else "utf-8"
            with open(fileName, "r", encoding=enc) as f:
                content = f.read()
            return MyQFileDir.ReadResult(True, content)
        except LookupError:
            qCritical(f"MyQFileDir::WriteFile unknown codec [{encoding}]")
            return MyQFileDir.ReadResult(False, "")
        except FileNotFoundError:
            qCritical(f"MyQFileDir::ReadFile2 can't open file [{fileName}]")
            return MyQFileDir.ReadResult(False, "")
        except OSError:
            qCritical(f"MyQFileDir::ReadFile2 can't read file [{fileName}]")
            return MyQFileDir.ReadResult(False, "")
        except Exception:
            qCritical(f"MyQFileDir::Exception [{fileName}]")
            return MyQFileDir.ReadResult(False, "")