from PyQt5 import QtWidgets
import os
import datetime
import manipulation as mp
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import (QWidget, QPushButton,QMainWindow,
                             QHBoxLayout, QApplication,QAction,QFileDialog)

# Main window
class Customer(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = customerStack()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)
        self.setWindowTitle('Customer')

        self.show()

# Main UI with options on the left hand side
class customerStack(QWidget):
    def __init__(self):

        super(customerStack, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Purchase Car')
        self.leftlist.insertItem(2, 'View Car Stock')

        self.stack1 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack3UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack3)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500,350, 200, 200)
        self.setWindowTitle('Stock Management')
        self.show()


    def stack1UI(self): # ADD STOCK UI
        layout = QFormLayout()
        self.mes = QLabel()

        self.ok = QPushButton('Purchase Car', self)
        clear = QPushButton('Clear', self)

        self.stock_name = QLineEdit()
        layout.addRow("Stock Name", self.stock_name)

        self.stock_count = QLineEdit()
        layout.addRow("Quantity", self.stock_count)

        layout.addWidget(self.ok)
        layout.addWidget(clear)
        layout.addWidget(self.mes)

        self.ok.clicked.connect(self.on_click)

        # clear the data from the screen
        clear.clicked.connect(self.stock_name.clear)
        clear.clicked.connect(self.stock_count.clear)
        self.stack1.setLayout(layout)

    def on_click(self): # update car stock
        # remove quantity from Manufacturer stock
        stock_name_dec = self.stock_name.text().replace(' ','_').lower()
        stock_count_dec = -(int(self.stock_count.text()))

        # add quantity to Dealership stock
        stock_name_inc = self.stock_name.text().replace(' ','_').lower()
        stock_count_inc = (int(self.stock_count.text()))

        if (stock_count_dec and stock_count_inc > 0):
            mp.del_car_stock(stock_name_dec,stock_count_dec)
            message = mp.add_car_stock(stock_name_inc,stock_count_inc)
            self.mes.setText(message)
        else:
            self.mes.setText('Invalid quantity')


    def stack3UI(self): # VIEW MANUFACTURER STOCK UI
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("View Car Stock")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))



        layout.addWidget(self.View)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):
        # checks database for stock items
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)

        x = []
        x = mp.show_car_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Car Stock.')
        else:
            self.lbl3.setText('No valid information in database.')


    def display(self, i):
        self.Stack.setCurrentIndex(i)