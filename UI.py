import sys
 

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi

from main_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        
        self.pushButton.clicked.connect(self.rec)
        
        self.pushButton_2.clicked.connect(self.de_noise)
        
        
        
    
    
    
    def rec(self):
        
        import record_audio
        
        record_audio.record_to_file('demo.wav')
        
        
        
    def de_noise(self):
        
        import sound
        





if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
