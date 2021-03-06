import sys
import os 

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi

from main_ui import Ui_MainWindow

from playsound import playsound


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        
        self.pushButton.clicked.connect(self.rec)
        
        self.pushButton_2.clicked.connect(self.de_noise)
        
        self.pushButton_3.clicked.connect(self.tex)
        
        self.pushButton_4.clicked.connect(self.signlang)
        
    
    
    def rec(self):
        
        import record_audio
        
        record_audio.record_to_file('sound/demo.wav')
    
    
    def tex(self):
        
        import voice_to_text
        
        voice_to_text.read()
        
    
    def signlang(self):
        
        import sign_lang
        
        sign_lang.recognize()
    
        
        
    def de_noise(self):
        
        import denoise
        
        denoise.noise()
        
        file='predictions/demo.wav'
        
        if os.path.exists(file)==True:
            
            playsound('predictions/demo.wav')



if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
