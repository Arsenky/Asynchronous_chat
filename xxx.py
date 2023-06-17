import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor


class Ui_Form(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 442)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton01 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton01.setEnabled(True)
        self.pushButton01.setGeometry(QtCore.QRect(60, 350, 171, 61))
        self.pushButton01.setObjectName("pushButton01")
        self.textEdit01 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit01.setEnabled(True)
        self.textEdit01.setGeometry(QtCore.QRect(45, 40, 571, 251))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.textEdit01.setFont(font)
        # self.textEdit01.setStyleSheet("background-color: yellow;")
        self.textEdit01.setReadOnly(True)
        self.textEdit01.setObjectName("textEdit01")
        self.btnQuit = QtWidgets.QPushButton(self.centralwidget)
        self.btnQuit.setGeometry(QtCore.QRect(470, 380, 93, 28))
        self.btnQuit.setObjectName("btnQuit")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton01, self.textEdit01)
        MainWindow.setTabOrder(self.textEdit01, self.btnQuit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton01.setText(_translate("MainWindow", "Исполнить"))
        self.btnQuit.setText(_translate("MainWindow", "EXIT"))


# Объект, который будет перемещаться в другой поток
class Second(QtCore.QObject):
    running = False
    newTextAndColor = QtCore.pyqtSignal(str, object)  # Сигнал

    # Метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        ic = 0
        while ic < 10:  # True:
            ic += 1

            txt_str = f'{str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))}' \
                f' - поток 2, вариант 1 (синий {ic: d})'

            # Посылаю signal с новым текстом и цветом из другого потока
            self.newTextAndColor.emit(txt_str, QColor(0, 0, 255))

            QtCore.QThread.msleep(1000)

            txt_str = f'{str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))}' \
                f' - поток 2, вариант 2 (красный {ic: d})'

            # Посылаю signal с новым текстом и цветом из другого потока
            self.newTextAndColor.emit(txt_str, QColor(255, 0, 0))

            QtCore.QThread.msleep(1000)


class MyWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Используем кнопку для вызова записи другого текста и цвета
        self.ui.pushButton01.clicked.connect(self.addAnotherTextAndColor)

        self.ui.btnQuit.clicked.connect(app.quit)  # нопка завершения приложения

        # создаём поток
        self.thread = QtCore.QThread()
        
        # создаём объект, который будет перемещаться в другой поток
        self.second = Second()
        
        # перемещаем объект в другой поток
        self.second.moveToThread(self.thread)

        # после этого можно соединить сигналы от этого объекта со слотом в основном потоке GUI
        self.second.newTextAndColor.connect(self.addNewTextAndColor)

        # соедияем посланный сигнал для того, чтобы запустить метод run объекта другого потока
        self.thread.started.connect(self.second.run)

        # start thread
        self.thread.start()

    @QtCore.pyqtSlot(str, object)  # описание слота
    def addNewTextAndColor(self, string, color):
        self.ui.textEdit01.setTextColor(color)
        self.ui.textEdit01.append(string)

    def addAnotherTextAndColor(self):
        self.ui.textEdit01.setTextColor(QColor(0, 255, 0))  # зелёный        
        txt_str = f'{str(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))}' \
            f' - поток 2, вариант 3 (зелёный *)'
        self.ui.textEdit01.append(txt_str)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())



# отправить сообщение 
# завершить работу
# добавить контакт !
# удалить контакт !
# регистрация !
# принимать сообщения 