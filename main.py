import sqlite3
import sys
from os import startfile
from sys import argv, exit

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

from item import AddItem, ChangeItem  # диалоги для создания и редактирования элемента
from NewTable import NewTable  # диалог для создания новой таблицы
from parent_of_main import MainFromUi  # созданный при помощи pyuic5 class
from welcome import Welcome  # первое привествие
from contact import ContactInformation  # контактная информация


class Main(QMainWindow, MainFromUi):  # основной класс
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("LaunchApp")
        self.show()
        # далее идет проверка запускать ли приветствующее окно
        with open("data/flag.txt") as f:  # открытие .txt файла для проверки(если пустой - нет, если в нём "..." - да)
            if not f.read():  # проверяется нажимал ли пользователь на галочку "больше не показывать"
                self.welcome = Welcome()  # если условие выполнилось открывается приветствие
                self.welcome.show()  # код класса в другом файле

        # далее будет показано подключение кнопкок к методам
        self.pushButton_run.clicked.connect(self.run)  # кнопка запуска приложений
        self.description.triggered.connect(self.open_description)  # описание приложения(в менюбаре)
        self.developer.triggered.connect(self.open_contact_information)  # контак. инф. (в менюбаре)
        self.pushButton_new.clicked.connect(self.create_table)  # кнопка создания нового раздела
        self.pushButton_add_item.clicked.connect(self.add_item)  # кнопка добавления элем. в раздел
        self.pushButton_change_item.clicked.connect(self.change_item)  # кнопка изменения элем. в разделе
        self.pushButton_open.clicked.connect(self.open_table)  # кнопка открытия раздела(таблицы)
        self.pushButton_del.clicked.connect(self.del_table)  # кнопка удаления раздела(таблицы)
        self.pushButton_del_item.clicked.connect(self.del_item)  # кнопка удаления элемента в разделе
        self.con = sqlite3.connect("LaunchApp.sqlite")  # подключение к базе данных
        self.cur = self.con.cursor()  # создание курсора
        self.res = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # сверху идёт запрос на получение названий всех разделов
        for i in self.res:  # добавление в comboBox всех названий
            if i[0] != "sqlite_sequence":
                self.comboBox.addItem(i[0])
        with open("data/last_table.txt", "r", encoding="utf-8") as f:  # получаем название последней открытой таблицы
            self.last_table = f.read().strip()
            if self.last_table:
                self.current_table = self.last_table
        self.comboBox.setCurrentIndex(self.comboBox.findText(self.current_table))  # выбираем посл. откр. таблицу
        self.update_table()  # обращение к методу для заполнения таблицы

    def run(self):  # запуск приложений
        self.pathes = [path_[0] for path_ in  # получение путей к приложениям
                       self.cur.execute(f'''SELECT "Путь" FROM "{self.comboBox.currentText()}"''')]
        for path_ in self.pathes:
            try:
                startfile(path_)  # запуск приложений
            except Exception:
                self.statusbar.showMessage(f"Нет приложения на пути {path_}")

    def open_description(self):  # запуск описания
        startfile(r'Презентация, ТЗ и ПЗ\Пояснительная записка.docx')

    def open_contact_information(self):  # диалог с контактной информацией
        self.widget = ContactInformation()
        self.widget.show()

    def open_table(self):  # метод для запуска раздела
        self.last_open_table(self.comboBox.currentText())  # сохранение последней запущенной таблицы
        self.update_table()  # обновление таблицы

    def create_table(self):  # метод для создания нового раздела
        self.widget = NewTable(self)  # диалог для создания нового раздела
        self.widget.show()

    def del_table(self):  # метод для удаления раздела
        self.message_box = QMessageBox()  # MessageBox для уточнения удаления
        self.message_box.setWindowTitle("Удаления раздела")  # заголовок
        self.message_box.setText(f"Вы уверенны что хотите удалить раздел: {self.comboBox.currentText()}?")  # вопрос
        self.message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # создание кнопкок Yes/No
        self.message_box.buttonClicked.connect(self.del_or_no)  # обращение к методу при нажатии на кнопку
        self.message_box.exec()

    def add_item(self):  # метод для создания нового элемента
        self.widget = AddItem(self)  # диалог для создания нового элемента
        self.widget.show()

    def change_item(self):  # метод для редактирования элемента
        self.statusbar.showMessage("")
        self.row = list(set([i.row() for i in self.tableWidget.selectedItems()]))  # выбранные строки в таблице
        if not self.row:  # проверка выбрана ли хоть какая-то строка
            self.statusbar.showMessage("НЕ ВЫБРАНА ЯЧЕЙКА      " * 6)
        else:
            self.row = self.row[0]  # первый выбранный элемент
            self.select_data = [self.tableWidget.item(self.row, i).text() for i in range(3)]  # данные выбр. элем
            self.widget = ChangeItem(self)  # диалог для редактирования элемента
            self.widget.show()

    def last_open_table(self, title):  # метод для сохранения в .txt файл последнего выбранного раздела
        with open("data/last_table.txt", "w", encoding="utf8", newline="") as f:
            f.write(title)

    def update_table(self):  # заполнение данных в TableWidget
        self.res = self.cur.execute(f'''SELECT * FROM "{self.comboBox.currentText()}"''').fetchall()
        self.headerName = [i[1] for i in  # названия заголовков таблицы
                           self.cur.execute(f"PRAGMA table_info('{self.comboBox.currentText()}')").fetchall()]
        # далее идет заполение таблицы
        self.tableWidget.setColumnCount(len(self.headerName))
        self.tableWidget.setHorizontalHeaderLabels(self.headerName)
        self.len_res = len(self.res)
        self.tableWidget.setRowCount(self.len_res)
        for i, elem in enumerate(self.res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()
        # далее идет растягивание столбцов
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def del_or_no(self, btn):  # метод обрабатывающий Yes/No при удалении таблицы
        if btn.text() == "&Yes":
            self.cur.execute(f"DROP TABLE '{self.comboBox.currentText()}'")  # удаление таблицы из базы данных
            self.con.commit()  # сохранение
            self.comboBox.clear()  # очищение comboBox
            # получение имен всех таблиц в базе данных
            self.res = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            # заполение имент разделов в comboBox
            for i in self.res:
                if i[0] != "sqlite_sequence":
                    print(i[0])
                    self.comboBox.addItem(i[0])

            self.comboBox.setCurrentIndex(self.comboBox.findText(self.res[-1][0]))  # выбор таблицы которая
            # стояла перед удаленной таблицой
            self.last_open_table(self.comboBox.currentText())  # сохрание в файл названия выбранной талицы
            self.update_table()  # заполение данных в TableWidget

    def del_item(self):  # удаления элемента
        self.statusbar.showMessage("")
        self.row = list(set([i.row() for i in self.tableWidget.selectedItems()]))  # выбранные строки в таблице
        if not self.row:  # проверка выбрана ли хоть какая-то строка
            self.statusbar.showMessage("НЕ ВЫБРАНА ЯЧЕЙКА      " * 6)
        else:
            self.row = self.row[0]  # первый выбранный элемент
            self.select_data = [self.tableWidget.item(self.row, i).text() for i in range(3)]  # данные выбр. элем
            self.cur.execute(f'''DELETE from {self.comboBox.currentText()}
            WHERE "ID" = {self.select_data[0]}''')  # удаление элемента
            self.con.commit()  # сохранение
            self.update_table()  # заполение данных в TableWidget


def except_hook(cls, exception, traceback):  # чтобы показывались ошибки на всякий случай
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(argv)
    window = Main()
    sys.excepthook = except_hook
    exit(app.exec())
