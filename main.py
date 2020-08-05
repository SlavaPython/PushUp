import datetime
import sys
from PyQt5 import QtWidgets
import design
from math import ceil
import os
import getpass


class AchieveApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        """Это здесь нужно для доступа к переменным, методам
        и т.д. в файле design.py"""
        super().__init__()
        self.setupUi(self)
        self.platform = sys.platform
        self.buttonOne.clicked.connect(self.day_achieve)
        self.today = str(datetime.datetime.now())[:10]
        self.target = 140
        self.name = getpass.getuser()
        self.app_folder = self.set_folder()
        self.day_value = self.day_value_f() or 0
        self.day_achieve()

    def day_achieve(self):
        """Возвращает все результаты и выполняет логирование"""
        self.day_quantity()
        self.progress_percentage()
        self.logs()

    def day_quantity(self):
        """Считает дневной результат"""
        self.day_value += self.click_value_f()
        self.lcdNumber.display(self.day_value)

    def click_value_f(self):
        """Текущее зачение клика"""
        current_value = self.spinBox.value()
        return current_value

    def progress_percentage(self):
        """Считает проценты выполнения"""
        if self.day_value > self.target:
            self.progressBar.setValue(100)
        day_percentage = (self.day_value / self.target) * 100
        self.set_percentage_bar_value(ceil(day_percentage))

    def set_percentage_bar_value(self, percentage: int):
        """Работа progressbar'а"""
        self.progressBar.setValue(percentage)

    def mk_dir(self):
        """Создание папок, если их ещё нет"""
        os.makedirs(self.app_folder)

    def logs(self):
        """Фиксирование результатов"""
        if os.path.exists(self.app_folder):
            os.chdir(self.app_folder)
            with open(f'{self.today}.txt', 'a') as log:
                log.write(f'{self.click_value_f()}\n')

        else:
            self.mk_dir()
            self.logs()

    def day_value_f(self):
        """Возвращает сегоднешний результат, если он уже есть, либо False"""
        try:
            os.chdir(self.app_folder)
            with open(rf'{self.today}.txt', 'r') as log:
                data = log.readlines()
                full = 0
                for line in data:
                    full += int(line)
            return full

        except FileNotFoundError:
            return False

    def set_folder(self):
        """Возвращает папку для логов соответсвенно оперативной системе"""
        if self.platform == "linux" or self.platform == "linux2":
            folder = rf'/home/{self.name}/PushUpApp/Logs/'
        elif self.platform == "darwin":
            pass  # OS X
        elif self.platform == "win32":
            folder = rf'C:\Users\{self.name}\Documents\Logs'
        return folder


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AchieveApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
