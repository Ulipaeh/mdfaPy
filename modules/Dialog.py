from PyQt5.QtWidgets import (QDialog ,QLabel, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

class Dialog(QDialog):
    def __init__(self, label, icon):
        super().__init__()
        lay = QtWidgets.QVBoxLayout(self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        
        self.icon = icon
        self.setWindowIcon(QIcon(self.icon))
        
        self.setWindowTitle('Message')
        self.label = label

        lbl = QLabel(self.label)

        dialogbutton = QDialogButtonBox()
        dialogbutton.setOrientation(Qt.Horizontal)
        dialogbutton.setStandardButtons(QDialogButtonBox.Ok)

        lay.addWidget(lbl)
        lay.addWidget(dialogbutton)

        dialogbutton.accepted.connect(self.accept)
        dialogbutton.rejected.connect(self.reject)
                
