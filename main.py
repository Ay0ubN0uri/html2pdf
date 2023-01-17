import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from main_ui import Ui_MainWindow
import sys
import os
import time
import pdfkit  

# configuring pdfkit to point to our installation of wkhtmltopdf
if sys.platform == "win32":
    config = pdfkit.configuration(wkhtmltopdf = os.path.join(os.path.dirname(__file__),'wkhtmltopdf.exe'))
else:
    config = pdfkit.configuration(wkhtmltopdf = '/usr/bin/wkhtmltopdf')
  


class ProgressBarUpdater(QThread):
    progressBarValue = pyqtSignal(int)
    open_folder_btn_visibility = pyqtSignal(bool)
    
    def __init__(self,myapp_obj):
        QThread.__init__(self)
        self.myapp_obj = myapp_obj

    def run(self):
        self.startConversion()
            
    def startConversion(self):
        self.myapp_obj.files = list(set(self.myapp_obj.files))
        self.myapp_obj.PutMessage('progress','Please Wait...')
        i = 1
        step = 100/len(self.myapp_obj.files)
        value = step
        for file in self.myapp_obj.files:
            if self.myapp_obj.isValidURL(file):
                pdfkit.from_url(file, os.path.join(self.myapp_obj.output_folder,f'url{i}.pdf'), configuration = config)
            else:
                file_name = os.path.basename(file)
                pdfkit.from_file(file, os.path.join(self.myapp_obj.output_folder,os.path.splitext(file_name)[0]+".pdf"), configuration = config)
            self.progressBarValue.emit(value)
            value = int(value + step)
        self.progressBarValue.emit(int(value))
        self.myapp_obj.PutMessage('success',"Finished")
        self.open_folder_btn_visibility.emit(True)


class MyApplication(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__),'icon.png')))
        self.input_files = []
        self.output_folder = os.path.dirname(__file__)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.progressBar.hide()
        self.ui.open_folder_btn.hide()
        self.ui.lineEdit_output_folder.setText(os.path.dirname(__file__))
        self.ui.checkBox.stateChanged.connect(self.checkbox_changed)
        self.ui.input_file_btn.clicked.connect(self.input_file_btn_clicked)
        self.ui.output_folder_btn.clicked.connect(self.output_folder_btn_clicked)
        self.ui.submit_btn.clicked.connect(self.submit_btn_clicked)
        self.ui.open_folder_btn.clicked.connect(self.open_folder_btn_clicked)
    
    def open_folder_btn_clicked(self):
        fullpath = os.path.realpath(self.output_folder)
        if not QDesktopServices.openUrl(QUrl.fromLocalFile(fullpath)):
            print("failed")

    def setVisibility_open_folder_btn(self,state):
        self.ui.open_folder_btn.show() if state else self.ui.open_folder_btn.hide()
            

    def submit_btn_clicked(self):
        self.ui.progressBar.setValue(0)
        self.ui.open_folder_btn.hide()
        self.input_urls = []
        self.files = []
        if self.ui.checkBox.isChecked():
            if self.ui.textEdit_url.toPlainText()=='':
                QMessageBox.warning(self, "Empty Field", "Please Enter Urls")
                return
            for url in self.ui.textEdit_url.toPlainText().strip().split('\n'):
                if not self.isValidURL(url):
                    QMessageBox.warning(self, "Invalid Urls", "Please Enter Valid Urls")
                    return
            self.input_urls = self.ui.textEdit_url.toPlainText().strip().split('\n')
            self.files=self.input_urls
        else:
            if len(self.input_files)==0:
                QMessageBox.warning(self, "Empty Field", "Please Choose Files")
                return
            self.files = self.input_files
        self.progressBarThread = ProgressBarUpdater(self)
        self.progressBarThread.progressBarValue.connect(self.update_value)
        self.progressBarThread.open_folder_btn_visibility.connect(self.setVisibility_open_folder_btn)
        self.progressBarThread.start()
        
    def startConversion(self):
        self.files = list(set(self.files))
        self.PutMessage('progress','Please Wait...')
        i = 1
        step = 100/len(self.files)
        value = step
        for file in self.files:
            if self.isValidURL(file):
                pdfkit.from_url(file, os.path.join(self.output_folder,f'url{i}.pdf'), configuration = config)
            else:
                file_name = os.path.basename(file)
                pdfkit.from_file(file, os.path.join(self.output_folder,os.path.splitext(file_name)[0]+".pdf"), configuration = config)
            self.update_value(value,step)
            time.sleep(0.1)
            value = int(value + step)
        self.update_value(value,step)
        self.PutMessage('success',"Finished")
        self.ui.open_folder_btn.show()
    
    def PutMessage(self,type,msg):
        self.messages = {
            'success':'green',
            'error':'red',
            'progress':'black'
        }
        self.ui.label_message.setText(msg)
        self.ui.label_message.setStyleSheet(f'color: {self.messages[type]}')
                
    def update_value(self, value,animated=True):
        if value>100:
            value = 100
        if animated:
            if hasattr(self, "animation"):
                self.animation.stop()
            else:
                self.animation = QPropertyAnimation(
                    targetObject=self.ui.progressBar, propertyName=b"value"
                )
                self.animation.setDuration(100)
            self.animation.setStartValue(self.ui.progressBar.value())
            self.animation.setEndValue(value)
            self.animation.start()
        else:
            self.ui.progressBar.setValue(value)
        
    def isValidURL(self,str):
        regex = ("((http|https)://)(www.)?" +
                "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                "{2,256}\\.[a-z]" +
                "{2,6}\\b([-a-zA-Z0-9@:%" +
                "._\\+~#?&//=]*)")
        p = re.compile(regex)
        if (str == None):
            return False
        if(re.search(p, str)):
            return True
        else:
            return False

    def output_folder_btn_clicked(self):
        tmp = QFileDialog.getExistingDirectory(self, caption='Choose Directory',directory=os.path.dirname(__file__))
        if tmp:
            self.output_folder = tmp
            self.ui.lineEdit_output_folder.setText(self.output_folder)
    
    def input_file_btn_clicked(self):
        self.input_files = []
        self.input_files.extend(QFileDialog.getOpenFileNames(self, caption='Choose Files',
                                                    directory=os.path.dirname(__file__),
                                                    filter='HTML Files (*.html)')[0])
        self.ui.lineEdit_input_file.setText(';'.join(self.input_files))

    def checkbox_changed(self):
        self.ui.input_file_btn.setEnabled(not self.ui.checkBox.isChecked())
        self.ui.textEdit_url.setEnabled(self.ui.checkBox.isChecked())


def main():
    app = QApplication(sys.argv)
    myApp = MyApplication()
    myApp.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()