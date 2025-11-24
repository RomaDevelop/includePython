from typing import List

from PySide6.QtCore import QStandardPaths, QFile, QFileInfo, QDir, QDateTime
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu,QWidget, QDialog, QMessageBox, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

from my_shortings import *
from MyQFileDir import *

class AppDataWork:
    RomaDevelop = "RomaDevelop"
    Catalog = "Catalog"

    @staticmethod
    def GetLinkFromAppData(appDataSubdir: str, programmName: str) -> str:
        fileExePath = AppDataWork.GetFolderInAppData(appDataSubdir, programmName) + "/exe_path_name.txt"

        if not QFileInfo(fileExePath).isFile():
            qmb_error("file " + fileExePath + " doesn't exist")
            return ""

        readRes = MyQFileDir.read_file(fileExePath)
        if not readRes.success:
            qmb_error("error reading " + fileExePath)
            return ""

        return readRes.content

    @staticmethod
    def GetFolderInAppData(appDataSubdir: str, programmName: str) -> str:
        appDataPath = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.GenericDataLocation)
        return f"{appDataPath}/{appDataSubdir}/{programmName}"

    @staticmethod
    def RemoveOldMessageFiles(folder):
        dir_ = QDir(folder)
        messagesFilesInfos = dir_.entryInfoList(["*MessageFileInAppData_*.txt"], QDir.Filter.Files)
        for msg_fi in messagesFilesInfos:
            if msg_fi.birthTime().secsTo(QDateTime.currentDateTime()) > 60 * 10:
                if not QFile.remove(msg_fi.absoluteFilePath()):
                    qmb_error("RemoveOldMessageFiles: error removing file " + msg_fi.absoluteFilePath())

    @staticmethod
    def WriteMessageFileInAppData(appDataSubdir, programmName, message):
        folder = AppDataWork.GetFolderInAppData(appDataSubdir, programmName)

        AppDataWork.RemoveOldMessageFiles(folder)

        if not QFileInfo(folder).isDir():
            qmb_error("WriteMessageFileInAppData: Destination folder " + folder + " doesn't exist")
            return

        preparing_ = "preparing_"

        filePreparing = folder + "/" + preparing_ + "MessageFileInAppData_" + \
                        QDateTime.currentDateTime().toString(DateTimeFormatForFileName_ms) + ".txt"
        fileReady = folder + "/" + "MessageFileInAppData_" + \
                    QDateTime.currentDateTime().toString(DateTimeFormatForFileName_ms) + ".txt"

        if not MyQFileDir.write_file(filePreparing, message):
            qmb_error("error writing " + filePreparing)
        else:
            if not QFile.rename(filePreparing, fileReady):
                qmb_error("error renaming file " + filePreparing + " to " + fileReady)