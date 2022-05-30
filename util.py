from PyQt5.QtWidgets import QMessageBox

'''
Icon types:
1 - Information
2 - Warning
3 - Critical
4 - Question
'''


def showMessage(title,messageType,messageText):
    message_dialog = QMessageBox()
    message_dialog.setWindowTitle(title)
    message_dialog.setIcon(messageType)
    message_dialog.setText(messageText)
    message_dialog.setStandardButtons(QMessageBox.Ok)
    message_dialog.setMinimumWidth(110)
    message_dialog.setStyleSheet("QMessageBox{text-align:left }")
    message_dialog.exec_()