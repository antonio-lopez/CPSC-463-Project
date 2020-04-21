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
class Dealership(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = dealershipStack()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)
        self.setWindowTitle('Dealership')

        self.show()

# Main UI with options on the left hand side
class dealershipStack(QWidget):
    def __init__(self):

        super(dealershipStack, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Add Stock')
        self.leftlist.insertItem(1, 'Manage Stock')
        self.leftlist.insertItem(2, 'Dealer Stock')
        self.leftlist.insertItem(4, 'Manufacturer Stock')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack5 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack5UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
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
        self.add_mes = QLabel()

        self.ok = QPushButton('Add Stock', self)
        clear = QPushButton('Clear', self)

        self.stock_name = QLineEdit()
        layout.addRow("Stock Name", self.stock_name)

        self.stock_count = QLineEdit()
        layout.addRow("Quantity", self.stock_count)

        # self.stock_cost = QLineEdit()
        # layout.addRow("Cost of Stock (per item)", self.stock_cost)

        layout.addWidget(self.ok)
        layout.addWidget(clear)
        layout.addWidget(self.add_mes)
        self.ok.clicked.connect(self.on_click)

        # clear the data from the screen
        clear.clicked.connect(self.stock_name.clear)
        #clear.clicked.connect(self.stock_cost.clear)
        clear.clicked.connect(self.stock_count.clear)
        self.stack1.setLayout(layout)

    def on_click(self): # Add user input data to the database when ADD STOCK button is pressed
        stock_name_inp = self.stock_name.text().replace(' ','_').lower()
        stock_count_inp = int(self.stock_count.text())
        #stock_cost_inp = int(self.stock_cost.text())
        if (stock_count_inp > 0):
            message = mp.insert_dealer_prod(stock_name_inp,stock_count_inp)
            self.add_mes.setText(message)
        else:
            self.add_mes.setText('Invalid quantity')


    def stack2UI(self): # MANAGE STOCK UI with 3 tab options

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0,300,1150,500))
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        tabs.addTab(self.tab1, 'Add Quantity')
        tabs.addTab(self.tab2, 'Reduce Quantity')
        tabs.addTab(self.tab3, 'Delete Stock')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        layout.addWidget(tabs)
        self.stack2.setLayout(layout)

    def tab1UI(self):   #ADD QUANTITY TAB
        layout = QFormLayout()
        self.ok_add = QPushButton('Add Stock', self)
        clear = QPushButton('Clear', self)
        self.mes1 = QLabel()

        self.stock_name_add = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_add)

        self.stock_count_add = QLineEdit()
        layout.addRow("Quantity to add", self.stock_count_add)

        layout.addWidget(self.ok_add)
        layout.addWidget(clear)
        layout.addWidget(self.mes1)
        #self.tab1.setLayout(layout)

        self.ok_add.clicked.connect(self.call_add)
        clear.clicked.connect(self.stock_name_add.clear)
        clear.clicked.connect(self.stock_count_add.clear)
        self.tab1.setLayout(layout)

    def tab2UI(self):   # REDUCE QUANTITY TAB
        layout = QFormLayout()
        self.mes2 = QLabel()
        self.ok_red = QPushButton('Reduce Stock', self)
        clear = QPushButton('Clear', self)

        self.stock_name_red = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Quantity to reduce", self.stock_count_red)


        layout.addWidget(self.ok_red)
        layout.addWidget(clear)
        layout.addWidget(self.mes2)
        self.tab2.setLayout(layout)

        self.ok_red.clicked.connect(self.call_red)
        clear.clicked.connect(self.stock_name_red.clear)
        clear.clicked.connect(self.stock_count_red.clear)

    def tab3UI(self):   # DELETE STOCK TAB
        layout = QFormLayout()
        self.mes3 = QLabel()
        self.ok_del = QPushButton('Delete Stock', self)
        clear = QPushButton('Clear', self)

        self.stock_name_del = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(clear)
        layout.addWidget(self.mes3)
        self.tab3.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del)
        clear.clicked.connect(self.stock_name_del.clear)

    def call_del(self):
        # deletes the stock item that is passed
        # needs a check test to see if item is in database
        # needs user notification if item was deleted successfully or item not found
        stock_name = self.stock_name_del.text().replace(' ','_').lower()
        message = mp.remove_dealer_stock(stock_name)
        self.mes3.setText(message)

    def call_red(self):
        # reduces the stock item quantity it is passed
        # needs a check test to see if item is in database
        # needs user notification if item quantity was reduced successfully or item not found
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        #stock_val = -(int(self.stock_count_red.text()))
        stock_val = int(self.stock_count_red.text())

        if (stock_val > 0):
            message = mp.dec_dealer_quantity(stock_name, stock_val)
            self.mes2.setText(message)
        else:
            self.mes2.setText('Invalid quantity')



    def call_add(self):
        # increases the stock item quantity it is passed
        # needs a check test to see if item is in database
        # needs user notification if item quantity was increased successfully or item not found
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())

        if (stock_val > 0):
            message = mp.inc_dealer_quantity(stock_name, stock_val)
            self.mes1.setText(message)
        else:
            self.mes1.setText('Invalid quantity')


    def stack3UI(self): # VIEW DEALERSHIP STOCK TAB
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
        self.srb.clicked.connect(self.show_dealer_search)
        self.stack3.setLayout(layout)

    def show_dealer_search(self):
        # checks database for stock items
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_dealer_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_dealer_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Dealership Stock Database.')
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


        x_act = mp.show_stock()
        x = []
        if self.conf_text5.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text5.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_stock()

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