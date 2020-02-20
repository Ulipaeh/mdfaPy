# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:24:20 2019

@author: Ulises
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QLabel, QDialog, QDialogButtonBox, QVBoxLayout)
from PyQt5.QtCore import Qt


class Dialog(QDialog):
    def __init__(self, label, icon):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)

        self.icon = icon
        self.setWindowIcon(QIcon(self.icon))
        
        self.setWindowTitle('Message')
        self.label = label

        lbl = QLabel(self.label)
        lbl.setStyleSheet("font-size: 20px")

        dialogbutton = QDialogButtonBox()
        dialogbutton.setOrientation(Qt.Horizontal)
        dialogbutton.setStandardButtons(QDialogButtonBox.Ok)

        layout.addWidget(lbl)
        layout.addWidget(dialogbutton)

        dialogbutton.accepted.connect(self.accept)
        dialogbutton.rejected.connect(self.reject)
