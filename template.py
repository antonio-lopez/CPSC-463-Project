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

import dealership as deal
import manufacturer as manufact
import customer as cust
import repairshop as repair

import sqlite3

# create database
try:
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # The manufacturing facilities are losing track of parts and materials 
    # and need a software tool to track all the car parts and materials (e.g. glass, bolts, chairs, steel) 
    # that have been purchased and received from suppliers.  They may have over 100 different suppliers.
    c.execute("""CREATE TABLE manufrStock (
                name text,
                quantity integer,
                cost integer
                ) """)
    # Car dealerships need new software to order new cars from the car manufacturer.
    # Repair shops, auto stores, and dealerships need to be able to order 
    # parts from the car manufacturer to keep their stock from running out 
    c.execute("""CREATE TABLE dealerStock (
                name text,
                quantity integer,
                cost integer
                ) """)
    c.execute("""CREATE TABLE shopPartStock (
                name text,
                quantity integer,
                cost integer
                ) """)
    # Customers need a way to order new and used cars directly from the 
    # car manufacturer that can then be picked up at a local dealership
    # Solution - no need for customer database, remove car inventory from
    # Manufacturer table and add to Dealership car inventory table  
    conn.commit()
except Exception:
    print('DB exists')


# login screen
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Admin Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)


    def handleLogin(self):
        # manufacturer
        if (self.textName.text() == 'Manu' and
            self.textPass.text() == '1111'):
            self.accept()
            self.manufacturer = manufact.Manufacturer()

        # dealership
        elif (self.textName.text() == 'Deal' and
            self.textPass.text() == '2222'):
            self.accept()
            self.dealership = deal.Dealership()

        # customer
        elif (self.textName.text() == 'Cust' and
            self.textPass.text() == '3333'):
            self.accept()
            self.customer = cust.Customer()

        # repair shop
        elif (self.textName.text() == 'Repair' and
            self.textPass.text() == '4444'):
            self.accept()
            self.repairshop = repair.Repairshop()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

# Register User screen - todo for later