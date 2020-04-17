from template import *

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    #register = Register()      #todo for later
    #if register.exec_() == QtWidgets.QDialog.Accepted: # todo for later

    if login.exec_() == QtWidgets.QDialog.Accepted: # opens login window
        # opens respective user window (manufacturer, customer, dealership, or repairshop)
        sys.exit(app.exec_())
