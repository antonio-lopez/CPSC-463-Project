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
class Repairshop(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = repairshopStack()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)
        self.setWindowTitle('Repairshop')

        self.show()

# Main UI with options on the left hand side
class repairshopStack(QWidget):
    def __init__(self):

        super(repairshopStack, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Order Stock')
        self.leftlist.insertItem(2, 'View Shop Stock')
        self.leftlist.insertItem(4, 'Manufacturer Stock')

        self.stack1 = QWidget()
        self.stack3 = QWidget()
        self.stack5 = QWidget()

        self.stack1UI()
        self.stack3UI()
        self.stack5UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack5)

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

        self.ok = QPushButton('Order Stock', self)
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

        # add quantity to Shop stock
        stock_name_inc = self.stock_name.text().replace(' ','_').lower()
        stock_count_inc = (int(self.stock_count.text()))

        if (stock_count_dec and stock_count_inc > 0):
            mp.del_shop_stock(stock_name_dec,stock_count_dec)
            message = mp.add_shop_stock(stock_name_inc,stock_count_inc)
            self.mes.setText(message)
        else:
            self.mes.setText('Invalid quantity')


    def stack3UI(self): # VIEW SHOP STOCK TAB
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Get Search Result.")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))

        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):
        # checks database for stock items
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_shop_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_shop_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Stock Database.')
        else:
            self.lbl3.setText('No valid information in database.')


    def stack5UI(self): # VIEW MANUFACTURER STOCK TAB
        layout_manu = QVBoxLayout()
        self.srb5 = QPushButton()
        self.srb5.setText("Get Search Result.")
        self.View5 = QTableWidget()
        self.lbl5 = QLabel()
        self.lbl_conf_text5 = QLabel()
        self.lbl_conf_text5.setText("Enter the search keyword:")
        self.conf_text5 = QLineEdit()

        self.View5.setColumnCount(3)
        self.View5.setColumnWidth(0, 250)
        self.View5.setColumnWidth(1, 250)
        self.View5.setColumnWidth(2, 200)
        self.View5.insertRow(0)
        self.View5.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View5.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View5.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))



        layout_manu.addWidget(self.View5)
        layout_manu.addWidget(self.lbl_conf_text5)
        layout_manu.addWidget(self.conf_text5)
        layout_manu.addWidget(self.srb5)
        layout_manu.addWidget(self.lbl5)
        self.srb5.clicked.connect(self.show_manu_search)
        self.stack5.setLayout(layout_manu)

    def show_manu_search(self):
        # checks database for stock items
        if self.View5.rowCount()>1:
            for i in range(1,self.View5.rowCount()):
                self.View5.removeRow(1)


        x_act = mp.show_manu_order_stock()
        x = []
        if self.conf_text5.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text5.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_manu_order_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View5.insertRow(i)
                a = list(x[i-1])
                self.View5.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View5.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View5.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View5.setRowHeight(i, 50)
            self.lbl5.setText('Viewing Manufacturer Stock Database.')
        else:
            self.lbl5.setText('No valid information in database.')

 
    def display(self, i):
        self.Stack.setCurrentIndex(i)